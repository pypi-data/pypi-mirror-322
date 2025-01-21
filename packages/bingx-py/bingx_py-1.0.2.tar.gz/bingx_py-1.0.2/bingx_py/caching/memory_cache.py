import asyncio
import threading
import time
from typing import Any, Optional

from .base import BaseAsyncCache, BaseCache


class SyncMemoryCache(BaseCache):
    """Synchronous in-memory cache implementation.

    This class provides a thread-safe synchronous in-memory cache implementation.
    It provides methods to set and get data with optional TTL (time-to-live) support.
    """

    def __init__(self) -> None:
        """Initialize the SyncMemoryCache.

        Returns
        -------
            None

        """
        self._data: dict[str, tuple[dict[str, Any], Optional[float]]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[dict[str, Any]]:
        """Get a value from the cache.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Optional[dict[str, Any]]: The value associated with the key, or None if not found or expired.

        """
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return None
            value, expires = entry
            if expires and expires < time.time():
                self._data.pop(key)
                return None
            return value

    def set(self, key: str, value: dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set a value in the cache.

        Args:
            key (str): The key to associate the value with.
            value (dict[str, Any]): The value to store.
            ttl (Optional[int]): The time-to-live in seconds. Defaults to None.

        Returns:
            None

        """
        with self._lock:
            expires = time.time() + ttl if ttl else None
            self._data[key] = (value, expires)


class AsyncMemoryCache(BaseAsyncCache):
    """Asynchronous in-memory cache implementation.

    This class provides an async-safe in-memory cache implementation.
    It provides methods to set and get data with optional TTL (time-to-live) support.
    """

    def __init__(self) -> None:
        """Initialize the AsyncMemoryCache.

        Returns
        -------
            None

        """
        self._data: dict[str, tuple[dict[str, Any], Optional[float]]] = {}
        self._lock = asyncio.Lock()

    async def aget(self, key: str) -> Optional[dict[str, Any]]:
        """Get a value from the cache asynchronously.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Optional[dict[str, Any]]: The value associated with the key, or None if not found or expired.

        """
        async with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return None
            value, expires = entry
            if expires and expires < time.time():
                del self._data[key]
                return None
            return value

    async def aset(
        self,
        key: str,
        value: dict[str, Any],
        ttl: Optional[int] = None,
    ) -> None:
        """Set a value in the cache asynchronously.

        Args:
            key (str): The key to associate the value with.
            value (dict[str, Any]): The value to store.
            ttl (Optional[int]): The time-to-live in seconds. Defaults to None.

        Returns:
            None

        """
        async with self._lock:
            expires = time.time() + ttl if ttl else None
            self._data[key] = (value, expires)
