from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    """Base class for synchronous caches.

    This class provides a basic interface for synchronous caches. It provides
    methods to set and get data from the cache, with optional TTL (time-to-live)
    support.
    """

    @abstractmethod
    def get(self, key: str) -> Optional[dict[str, Any]]:
        """Get data from the cache.

        Args:
            key (str): The key to retrieve from the cache.

        Returns:
            Optional[dict[str, Any]]: The retrieved data, or None if the key does not exist.

        """

    @abstractmethod
    def set(self, key: str, value: dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set data in the cache.

        Args:
            key (str): The key to set in the cache.
            value (dict[str, Any]): The data to set.
            ttl (Optional[int]): The time-to-live (TTL) for the data in seconds. If not provided, the data will not expire.

        Returns:
            None

        """


class BaseAsyncCache(ABC):
    """Base class for asynchronous caches.

    This class provides a basic interface for asynchronous caches. It provides
    methods to set and get data from the cache, with optional TTL (time-to-live)
    support.
    """

    @abstractmethod
    async def aget(self, key: str) -> Optional[dict[str, Any]]:
        """Get data from the cache asynchronously.

        Args:
            key (str): The key to retrieve from the cache.

        Returns:
            Optional[dict[str, Any]]: The retrieved data, or None if the key does not exist.

        """

    @abstractmethod
    async def aset(
        self,
        key: str,
        value: dict[str, Any],
        ttl: Optional[int] = None,
    ) -> None:
        """Set data in the cache asynchronously.

        Args:
            key (str): The key to set in the cache.
            value (dict[str, Any]): The data to set.
            ttl (Optional[int]): The time-to-live (TTL) for the data in seconds. If not provided, the data will not expire.

        Returns:
            None

        """
