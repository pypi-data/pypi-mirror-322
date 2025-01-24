import os
from typing import Dict, Any
from twisted.internet import reactor
from log import logger

class S3StorageProvider:
    def __init__(self, config):
        self.media_store_path = config.get('media_store_path')
        self.bucket = config.get('bucket')
        self.prefix = config.get('prefix', '')
        self.store_local = config.get('store_local', False)
        self.local_media_lifetime = config.get('local_media_lifetime', 0)
        self.remote_media_lifetime = config.get('remote_media_lifetime', 0)
        self.uploads_path = config.get('uploads_path')
        self.extra_args = config.get('extra_args', {})
        self._pending_files = {}

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