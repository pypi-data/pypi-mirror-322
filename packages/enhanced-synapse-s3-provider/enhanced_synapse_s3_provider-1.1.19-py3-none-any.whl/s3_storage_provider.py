# -*- coding: utf-8 -*-
# Copyright 2018 New Vector Ltd
# Copyright 2021 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import threading
import asyncio
from typing import Dict, Any

from six import string_types

import boto3
import botocore

from twisted.internet import defer, reactor, threads
from twisted.python.failure import Failure
from twisted.python.threadpool import ThreadPool

from synapse.logging.context import LoggingContext, make_deferred_yieldable
from synapse.rest.media.v1._base import Responder
from synapse.rest.media.v1.storage_provider import StorageProvider

# Synapse 1.13.0 moved current_context to a module-level function.
try:
    from synapse.logging.context import current_context
except ImportError:
    current_context = LoggingContext.current_context

logger = logging.getLogger("synapse.s3")


# The list of valid AWS storage class names
_VALID_STORAGE_CLASSES = (
    "STANDARD",
    "REDUCED_REDUNDANCY",
    "STANDARD_IA",
    "INTELLIGENT_TIERING",
)

# Chunk size to use when reading from s3 connection in bytes
READ_CHUNK_SIZE = 16 * 1024


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
        # Try to get uploads_path from config, fallback to media_store_path/uploads
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
            # If config block is not present, try getting S3 settings from root level
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
            # Get settings from config block
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
        
        # Remove None values from api_kwargs
        self.api_kwargs = {k: v for k, v in self.api_kwargs.items() if v is not None}
        
        if self.prefix and not self.prefix.endswith("/"):
            self.prefix += "/"

        # Initialize S3 client
        self._s3_client = None
        self._s3_client_lock = threading.Lock()
        
        # Initialize thread pool for S3 operations
        self._s3_pool = ThreadPool(1)
        
        # Dictionary to track files pending deletion
        self._pending_files = {}
        
        # Start cleanup task
        self._start_cleanup_task()
        
        logger.info("S3 Storage Provider initialized with bucket: %s", self.bucket)
        logger.info("Using media_store_path: %s", self.media_store_path)
        logger.info("Using uploads_path: %s", self.uploads_path)
        if self.local_media_lifetime or self.remote_media_lifetime:
            logger.info(
                "Media retention configured - Local: %s seconds, Remote: %s seconds",
                self.local_media_lifetime or "not set",
                self.remote_media_lifetime or "not set"
            )

    def _cleanup_and_stop(self):
        """Clean up any remaining files and stop the thread pool"""
        self._cleanup_files()
        self._s3_pool.stop()

    def _start_cleanup_task(self):
        """Start a periodic task to clean up files after retention period"""
        def _cleanup():
            while True:
                self._cleanup_files()
                # Sleep for 30 seconds between checks
                reactor.callLater(30, _cleanup)
        
        reactor.callInThread(_cleanup)

    def _cleanup_files(self):
        """Check and clean up files that have exceeded their retention period"""
        current_time = reactor.seconds()
        files_to_delete = []

        # Find files that need to be deleted
        for path, (delete_time, is_local) in list(self._pending_files.items()):
            if current_time >= delete_time:
                files_to_delete.append((path, is_local))
                del self._pending_files[path]

        # Delete the files
        for path, is_local in files_to_delete:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    logger.info("Retention period expired, removed file: %s", path)
                    self._cleanup_empty_directories(path)
            except Exception as e:
                logger.error("Failed to clean up file %s: %s", path, str(e))

    def _get_s3_client(self):
        # this method is designed to be thread-safe, so that we can share a
        # single boto3 client across multiple threads.
        #
        # (XXX: is creating a client actually a blocking operation, or could we do
        # this on the main thread, to simplify all this?)

        # first of all, do a fast lock-free check
        s3 = self._s3_client
        if s3:
            return s3

        # no joy, grab the lock and repeat the check
        with self._s3_client_lock:
            s3 = self._s3_client
            if not s3:
                b3_session = boto3.session.Session()
                self._s3_client = s3 = b3_session.client("s3", **self.api_kwargs)
            return s3

    def store_file(self, path: str, file_info: Dict[str, Any]) -> None:
        """Store the file described by file_info at path.

        Args:
            path: Relative path where to store the file
            file_info: Dict containing relevant information about the file
        """
        # Skip if no media store path is configured
        if not self.media_store_path:
            logger.info("No media_store_path configured, skipping S3 upload for %s", path)
            return

        local_path = os.path.join(self.media_store_path, path)
        abs_path = os.path.abspath(local_path)
        
        # Determine if media is local based on path
        is_local = False
        if self.uploads_path and abs_path.startswith(os.path.abspath(self.uploads_path)):
            is_local = True
        elif self.media_store_path:
            rel_path = os.path.relpath(abs_path, self.media_store_path)
            is_local = any(p.startswith("local") for p in rel_path.split(os.sep))
        
        logger.info("Uploading %s to S3 bucket %s", path, self.bucket)
        
        try:
            s3_client = self._get_s3_client()
            with open(local_path, 'rb') as f:
                s3_client.upload_fileobj(
                    f,
                    self.bucket,
                    self.prefix + path,
                    ExtraArgs=self.extra_args
                )
            logger.info("Successfully uploaded %s to S3", path)
            
            # If store_local is false, always delete immediately after S3 upload
            if not self.store_local:
                logger.info("store_local is false, removing local file immediately: %s", local_path)
                try:
                    if os.path.exists(local_path):
                        os.remove(local_path)
                        self._cleanup_empty_directories(local_path)
                except Exception as e:
                    logger.error("Failed to remove local file %s: %s", local_path, str(e))
                return
            
            # If we get here, store_local is true - handle retention
            retention_period = self.local_media_lifetime if is_local else self.remote_media_lifetime
            
            logger.info(
                "Checking retention for %s - Type: %s, Path: %s, Retention period: %s",
                path,
                "local" if is_local else "remote",
                abs_path,
                retention_period or "not set"
            )
            
            # Only schedule deletion if retention period is set
            if retention_period:
                delete_time = reactor.seconds() + retention_period
                self._pending_files[abs_path] = (delete_time, is_local)
                logger.info(
                    "File %s scheduled for deletion at %s (in %s seconds)",
                    local_path,
                    delete_time,
                    retention_period
                )
            else:
                logger.info(
                    "No retention period set for %s media, keeping local file: %s",
                    "local" if is_local else "remote",
                    local_path
                )
                
        except Exception as e:
            logger.error("Failed to upload %s to S3: %s", path, str(e))
            raise

    def _cleanup_empty_directories(self, file_path: str) -> None:
        """Clean up empty directories after file deletion.
        
        Args:
            file_path: Path to the deleted file
        """
        try:
            current_dir = os.path.dirname(file_path)
            base_dir = self.uploads_path if (self.uploads_path and file_path.startswith(self.uploads_path)) else self.media_store_path
            
            while base_dir and current_dir.startswith(base_dir):
                try:
                    if os.path.exists(current_dir) and not os.listdir(current_dir):
                        os.rmdir(current_dir)
                        logger.info("Removed empty directory: %s", current_dir)
                    else:
                        break
                except OSError as e:
                    logger.warning("Failed to remove directory %s: %s", current_dir, str(e))
                    break
                current_dir = os.path.dirname(current_dir)
        except Exception as e:
            logger.error("Failed to clean up directories for %s: %s", file_path, str(e))

    def fetch(self, path, file_info):
        """See StorageProvider.fetch"""
        logcontext = current_context()

        d = defer.Deferred()

        def _get_file():
            s3_download_task(
                self._get_s3_client(), self.bucket, self.prefix + path, self.extra_args, d, logcontext
            )

        self._s3_pool.callInThread(_get_file)
        return make_deferred_yieldable(d)

    @staticmethod
    def parse_config(config):
        """Called on startup to parse config supplied. This should parse
        the config and raise if there is a problem.

        The returned value is passed into the constructor.

        In this case we return a dict with fields, `bucket`, `prefix`, `storage_class` and `media_retention`
        """
        bucket = config["bucket"]
        prefix = config.get("prefix", "")
        storage_class = config.get("storage_class", "STANDARD")

        assert isinstance(bucket, string_types)
        assert storage_class in _VALID_STORAGE_CLASSES

        result = {
            "bucket": bucket,
            "prefix": prefix,
            "extra_args": {"StorageClass": storage_class},
        }

        # Parse media retention settings
        if "media_retention" in config:
            result["media_retention"] = {
                "local_media_lifetime": config["media_retention"].get("local_media_lifetime"),
                "remote_media_lifetime": config["media_retention"].get("remote_media_lifetime")
            }

        if "region_name" in config:
            result["region_name"] = config["region_name"]

        if "endpoint_url" in config:
            result["endpoint_url"] = config["endpoint_url"]

        if "access_key_id" in config:
            result["access_key_id"] = config["access_key_id"]

        if "secret_access_key" in config:
            result["secret_access_key"] = config["secret_access_key"]

        if "session_token" in config:
            result["session_token"] = config["session_token"]

        if "sse_customer_key" in config:
            result["extra_args"]["SSECustomerKey"] = config["sse_customer_key"]
            result["extra_args"]["SSECustomerAlgorithm"] = config.get(
                "sse_customer_algo", "AES256"
            )

        return result


def s3_download_task(s3_client, bucket, key, extra_args, deferred, parent_logcontext):
    """Attempts to download a file from S3.

    Args:
        s3_client: boto3 s3 client
        bucket (str): The S3 bucket which may have the file
        key (str): The key of the file
        deferred (Deferred[_S3Responder|None]): If file exists
            resolved with an _S3Responder instance, if it doesn't
            exist then resolves with None.
        parent_logcontext (LoggingContext): the logcontext to report logs and metrics
            against.
    """
    with LoggingContext(parent_context=parent_logcontext):
        logger.info("Fetching %s from S3", key)

        try:
            if "SSECustomerKey" in extra_args and "SSECustomerAlgorithm" in extra_args:
                resp = s3_client.get_object(
                    Bucket=bucket,
                    Key=key,
                    SSECustomerKey=extra_args["SSECustomerKey"],
                    SSECustomerAlgorithm=extra_args["SSECustomerAlgorithm"],
                )
            else:
                resp = s3_client.get_object(Bucket=bucket, Key=key)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] in ("404", "NoSuchKey",):
                logger.info("Media %s not found in S3", key)
                reactor.callFromThread(deferred.callback, None)
                return

            reactor.callFromThread(deferred.errback, Failure())
            return

        producer = _S3Responder()
        reactor.callFromThread(deferred.callback, producer)
        _stream_to_producer(reactor, producer, resp["Body"], timeout=90.0)


def _stream_to_producer(reactor, producer, body, status=None, timeout=None):
    """Streams a file like object to the producer.

    Correctly handles producer being paused/resumed/stopped.

    Args:
        reactor
        producer (_S3Responder): Producer object to stream results to
        body (file like): The object to read from
        status (_ProducerStatus|None): Used to track whether we're currently
            paused or not. Used for testing
        timeout (float|None): Timeout in seconds to wait for consume to resume
            after being paused
    """

    # Set when we should be producing, cleared when we are paused
    wakeup_event = producer.wakeup_event

    # Set if we should stop producing forever
    stop_event = producer.stop_event

    if not status:
        status = _ProducerStatus()

    try:
        while not stop_event.is_set():
            # We wait for the producer to signal that the consumer wants
            # more data (or we should abort)
            if not wakeup_event.is_set():
                status.set_paused(True)
                ret = wakeup_event.wait(timeout)
                if not ret:
                    raise Exception("Timed out waiting to resume")
                status.set_paused(False)

            # Check if we were woken up so that we abort the download
            if stop_event.is_set():
                return

            chunk = body.read(READ_CHUNK_SIZE)
            if not chunk:
                return

            reactor.callFromThread(producer._write, chunk)

    except Exception:
        reactor.callFromThread(producer._error, Failure())
    finally:
        reactor.callFromThread(producer._finish)
        if body:
            body.close()


class _S3Responder(Responder):
    """A Responder for S3. Created by _S3DownloadThread
    """

    def __init__(self):
        # Triggered by responder when more data has been requested (or
        # stop_event has been triggered)
        self.wakeup_event = threading.Event()
        # Trigered by responder when we should abort the download.
        self.stop_event = threading.Event()

        # The consumer we're registered to
        self.consumer = None

        # The deferred returned by write_to_consumer, which should resolve when
        # all the data has been written (or there has been a fatal error).
        self.deferred = defer.Deferred()

    def write_to_consumer(self, consumer):
        """See Responder.write_to_consumer
        """
        self.consumer = consumer
        # We are a IPushProducer, so we start producing immediately until we
        # get a pauseProducing or stopProducing
        consumer.registerProducer(self, True)
        self.wakeup_event.set()
        return make_deferred_yieldable(self.deferred)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        self.wakeup_event.set()

    def resumeProducing(self):
        """See IPushProducer.resumeProducing
        """
        # The consumer is asking for more data, signal _S3DownloadThread
        self.wakeup_event.set()

    def pauseProducing(self):
        """See IPushProducer.stopProducing
        """
        self.wakeup_event.clear()

    def stopProducing(self):
        """See IPushProducer.stopProducing
        """
        # The consumer wants no more data ever, signal _S3DownloadThread
        self.stop_event.set()
        self.wakeup_event.set()
        if not self.deferred.called:
            self.deferred.errback(Exception("Consumer ask to stop producing"))

    def _write(self, chunk):
        """Writes the chunk of data to consumer. Called by _S3DownloadThread.
        """
        if self.consumer and not self.stop_event.is_set():
            self.consumer.write(chunk)

    def _error(self, failure):
        """Called when a fatal error occured while getting data. Called by
        _S3DownloadThread.
        """
        if self.consumer:
            self.consumer.unregisterProducer()
            self.consumer = None

        if not self.deferred.called:
            self.deferred.errback(failure)

    def _finish(self):
        """Called when there is no more data to write. Called by _S3DownloadThread.
        """
        if self.consumer:
            self.consumer.unregisterProducer()
            self.consumer = None

        if not self.deferred.called:
            self.deferred.callback(None)


class _ProducerStatus(object):
    """Used to track whether the s3 download thread is currently paused
    waiting for consumer to resume. Used for testing.
    """

    def __init__(self):
        self.is_paused = threading.Event()
        self.is_paused.clear()

    def wait_until_paused(self, timeout=None):
        is_paused = self.is_paused.wait(timeout)
        if not is_paused:
            raise Exception("Timed out waiting")

    def set_paused(self, paused):
        if paused:
            self.is_paused.set()
        else:
            self.is_paused.clear()
