import os
import threading
from typing import Dict, Any
from twisted.internet import reactor, defer, threads
from twisted.python.failure import Failure

import boto3
import logging

from synapse.logging.context import LoggingContext, make_deferred_yieldable
from synapse.rest.media.v1._base import Responder
from synapse.rest.media.v1.storage_provider import StorageProvider

# Try to import current_context from the new location, fall back to the old one
try:
    from synapse.logging.context import current_context
except ImportError:
    current_context = LoggingContext.current_context

logger = logging.getLogger("synapse.s3")

class S3StorageProviderBackend(StorageProvider):
    """Storage provider for S3 storage.

    Args:
        hs (HomeServer): Homeserver instance
        config: The config dict from the homeserver config
    """

    def __init__(self, hs, config):
        super().__init__(hs)
        self.hs = hs

        # Get paths from Synapse config
        self.media_store_path = hs.config.media.media_store_path
        try:
            self.uploads_path = hs.config.media.uploads_path
        except AttributeError:
            self.uploads_path = os.path.join(self.media_store_path, "uploads")
            logger.info("uploads_path not found in config, using: %s", self.uploads_path)

        self.cache_directory = self.media_store_path

        # Initialize storage settings from config
        self.store_local = config.get("store_local", True)
        self.store_remote = config.get("store_remote", True)
        self.store_synchronous = config.get("store_synchronous", True)

        # Get media retention settings
        media_retention = config.get("media_retention", {})
        self.local_media_lifetime = media_retention.get("local_media_lifetime")
        self.remote_media_lifetime = media_retention.get("remote_media_lifetime")

        # S3 configuration
        s3_config = config.get("config", {})
        if not s3_config:
            self.bucket = config.get("bucket")
            self.api_kwargs = {
                "region_name": config.get("region_name"),
                "endpoint_url": config.get("endpoint_url"),
                "aws_access_key_id": config.get("access_key_id"),
                "aws_secret_access_key": config.get("secret_access_key"),
            }
            self.prefix = config.get("prefix", "")
            self.extra_args = config.get("extra_args", {})
        else:
            self.bucket = s3_config.get("bucket")
            self.api_kwargs = {
                "region_name": s3_config.get("region_name"),
                "endpoint_url": s3_config.get("endpoint_url"),
                "aws_access_key_id": s3_config.get("access_key_id"),
                "aws_secret_access_key": s3_config.get("secret_access_key"),
            }
            self.prefix = s3_config.get("prefix", "")
            self.extra_args = s3_config.get("extra_args", {})

        if not self.bucket:
            raise Exception("S3 bucket must be specified either in config block or at root level")
        
        self.api_kwargs = {k: v for k, v in self.api_kwargs.items() if v is not None}
        
        if self.prefix and not self.prefix.endswith("/"):
            self.prefix += "/"

        self._s3_client = None
        self._s3_client_lock = threading.Lock()
        self._s3_pool = ThreadPool(1)
        self._pending_files = {}
        
        logger.info("S3 Storage Provider initialized with bucket: %s, store_local: %s", self.bucket, self.store_local)
        logger.info("Using media_store_path: %s", self.media_store_path)
        logger.info("Using uploads_path: %s", self.uploads_path)

    def _get_s3_client(self):
        """Get or create an S3 client."""
        if self._s3_client is None:
            with self._s3_client_lock:
                if self._s3_client is None:
                    self._s3_client = boto3.client("s3", **self.api_kwargs)
        return self._s3_client

    def _cleanup_empty_directories(self, path):
        """Recursively remove empty directories."""
        directory = os.path.dirname(path)
        while directory and directory.startswith(self.media_store_path):
            try:
                os.rmdir(directory)
                logger.debug("Removed empty directory: %s", directory)
            except OSError:
                break  # Directory not empty or already removed
            directory = os.path.dirname(directory)

    async def store_file(self, path: str, file_info: Dict[str, Any]) -> None:
        """Store a file in S3 and handle local storage based on config."""
        if not self.media_store_path:
            logger.info("No media_store_path configured, skipping S3 upload for %s", path)
            return

        local_path = os.path.join(self.media_store_path, path)
        abs_path = os.path.abspath(local_path)
        
        try:
            # Upload to S3
            s3_client = self._get_s3_client()
            with open(local_path, 'rb') as f:
                s3_client.upload_fileobj(
                    f,
                    self.bucket,
                    self.prefix + path,
                    ExtraArgs=self.extra_args
                )
            logger.info("Successfully uploaded %s to S3", path)

            # If store_local is false, always delete immediately regardless of retention
            if not self.store_local:
                if os.path.exists(local_path):
                    os.remove(local_path)
                    self._cleanup_empty_directories(local_path)
                    logger.info("store_local=false: Removed local file immediately after S3 upload: %s", local_path)
                return

            # If we get here, store_local is true
            # Only handle retention if it's configured, otherwise keep the file forever
            is_local = (self.uploads_path and abs_path.startswith(os.path.abspath(self.uploads_path))) or \
                      any(p.startswith("local") for p in os.path.relpath(abs_path, self.media_store_path).split(os.sep))

            retention_period = self.local_media_lifetime if is_local else self.remote_media_lifetime
            if retention_period:
                delete_time = reactor.seconds() + retention_period
                self._pending_files[abs_path] = (delete_time, is_local)
                logger.info(
                    "store_local=true with retention: File %s will be deleted after %s seconds",
                    local_path,
                    retention_period
                )
            else:
                logger.info(
                    "store_local=true without retention: File %s will be kept indefinitely",
                    local_path
                )
                
        except Exception as e:
            logger.error("Failed to process %s: %s", path, str(e))
            raise 