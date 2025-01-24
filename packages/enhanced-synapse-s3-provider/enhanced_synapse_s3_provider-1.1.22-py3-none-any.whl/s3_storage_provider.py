import os
import threading
from typing import Dict, Any
from twisted.internet import reactor
from synapse.logging.context import LoggingContext
from synapse.storage.media.media_storage import MediaStorage
from synapse.storage.media.storage_provider import StorageProvider
from synapse.logging.context import make_deferred_yieldable
from synapse.util.async_helpers import maybe_awaitable
import boto3
import logging

logger = logging.getLogger(__name__)

class S3StorageProviderBackend(StorageProvider):
    """
    Args:
        hs (HomeServer)
        config: The config returned by `parse_config`
    """

    def __init__(self, hs, config):
        super().__init__()
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
        # This method should be implemented to return an S3 client
        pass

    def _cleanup_empty_directories(self, path):
        # This method should be implemented to clean up empty directories
        pass

    async def store_temporary_file(self, path: str, file_info: Dict[str, Any]) -> None:
        """Store file temporarily, upload to S3, then delete immediately if store_local is false."""
        local_path = os.path.join(self.media_store_path, path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Write the file temporarily
        with open(local_path, "wb") as f:
            f.write(file_info["file_object"].read())

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

            # When store_local is false, always delete immediately regardless of retention
            if not self.store_local:
                if os.path.exists(local_path):
                    os.remove(local_path)
                    self._cleanup_empty_directories(local_path)
                    logger.info("store_local=false: Removed local file immediately after S3 upload: %s", local_path)
            
        except Exception as e:
            logger.error("Failed to process %s: %s", path, str(e))
            # Clean up temporary file if it exists
            if os.path.exists(local_path):
                os.remove(local_path)
            raise

    def store_file(self, path: str, file_info: Dict[str, Any]) -> None:
        """Store the file described by file_info at path."""
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