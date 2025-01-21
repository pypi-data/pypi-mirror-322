import json
from types import TracebackType
from typing import Any, Optional, Self

from redis.asyncio import Redis as AsyncRedis
from redis.client import Redis

from .base import BaseAsyncCache, BaseCache


class SyncRedisCache(BaseCache):
    """Synchronous Redis cache implementation.

    This class provides a synchronous Redis cache implementation using the
    `redis` library. It provides methods to set and get data from Redis, with
    optional TTL (time-to-live) support.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        """Initialize the SyncRedisCache.

        Args:
            host (str): The Redis host. Defaults to "localhost".
            port (int): The Redis port. Defaults to 6379.
            db (int): The Redis database number. Defaults to 0.

        Returns:
            None

        """
        self._client = Redis(host=host, port=port, db=db)

    def __del__(self) -> None:
        """Close the Redis connection.

        Returns
        -------
            None

        """
        self._client.close()

    def get(self, key: str) -> Optional[dict[str, Any]]:
        """Get data from Redis.

        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[dict[str, Any]]: The retrieved data, or None if the key does not exist.

        """
        data = self._client.get(key)
        if data is None:
            return None
        return json.loads(data)  # type: ignore

    def set(self, key: str, value: dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set data in Redis.

        Args:
            key (str): The key to set in Redis.
            value (dict[str, Any]): The data to set.
            ttl (Optional[int]): The time-to-live (TTL) for the data in seconds. If not provided, the data will not expire.

        Returns:
            None

        """
        data = json.dumps(value)
        if ttl:
            self._client.setex(key, ttl, data)
        else:
            self._client.set(key, data)


class AsyncRedisCache(BaseAsyncCache):
    """Asynchronous Redis cache implementation.

    This class provides an asynchronous Redis cache implementation using the
    `redis.asyncio` library. It provides methods to set and get data from Redis,
    with optional TTL (time-to-live) support.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        """Initialize the AsyncRedisCache.

        Args:
            host (str): The Redis host. Defaults to "localhost".
            port (int): The Redis port. Defaults to 6379.
            db (int): The Redis database number. Defaults to 0.

        Returns:
            None

        """
        self._client = AsyncRedis(host=host, port=port, db=db)

    async def __aenter__(self) -> Self:
        """Enter the asynchronous context manager.

        Returns
        -------
            self

        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the asynchronous context manager.

        Args:
            exc_type (Optional[type[BaseException]]): The exception type.
            exc_value (Optional[BaseException]): The exception value.
            traceback (Optional[TracebackType]): The traceback.

        Returns:
            None

        """
        await self._client.close()

    async def aget(self, key: str) -> Optional[dict[str, Any]]:
        """Get data from Redis asynchronously.

        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[dict[str, Any]]: The retrieved data, or None if the key does not exist.

        """
        data = await self._client.get(key)
        if data is None:
            return None
        return json.loads(data.decode("utf-8"))

    async def aset(
        self,
        key: str,
        value: dict[str, Any],
        ttl: Optional[int] = None,
    ) -> None:
        """Set data in Redis asynchronously.

        Args:
            key (str): The key to set in Redis.
            value (dict[str, Any]): The data to set.
            ttl (Optional[int]): The time-to-live (TTL) for the data in seconds. If not provided, the data will not expire.

        Returns:
            None

        """
        data = json.dumps(value)
        if ttl:
            await self._client.setex(key, ttl, data)
        else:
            await self._client.set(key, data)
