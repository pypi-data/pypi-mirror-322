from __future__ import annotations
from typing import Literal

from .caching.memory_cache import AsyncMemoryCache, SyncMemoryCache
from .caching.redis_cache import AsyncRedisCache, SyncRedisCache

# Supported cache types
CacheType = Literal["async-redis", "sync-redis", "async-memory", "sync-memory"]


class CacheConfig:
    """Configuration class for managing cache settings and instances.

    This avoids the use of global variables.
    """

    def __init__(self) -> None:
        self._cache: (
            AsyncMemoryCache | SyncMemoryCache | AsyncRedisCache | SyncRedisCache | None
        ) = SyncMemoryCache()
        self._unsafe_cache: bool = False

    def create_cache(
        self,
        cache_type: CacheType,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
    ) -> AsyncMemoryCache | SyncMemoryCache | AsyncRedisCache | SyncRedisCache:
        """Create a cache instance based on the type.

        Args:
            cache_type (CacheType): The type of cache to create.
            host (str): Redis host. Defaults to "localhost".
            port (int): Redis port. Defaults to 6379.
            db (int): Redis database number. Defaults to 0.

        Returns:
            AsyncMemoryCache | SyncMemoryCache | AsyncRedisCache | SyncRedisCache: The created cache instance.

        """
        if cache_type == "async-redis":
            return AsyncRedisCache(host=host, port=port, db=db)
        if cache_type == "sync-redis":
            return SyncRedisCache(host=host, port=port, db=db)
        if cache_type == "async-memory":
            return AsyncMemoryCache()
        if cache_type == "sync-memory":
            return SyncMemoryCache()
        return None

    def set_cache(
        self,
        cache_type: CacheType,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
    ) -> None:
        """Set the cache instance based on the configured cache type.

        Args:
            cache_type (CacheType): The type of cache to set.
            host (str): Redis host. Defaults to "localhost".
            port (int): Redis port. Defaults to 6379.
            db (int): Redis database number. Defaults to 0.

        """
        self._cache = self.create_cache(cache_type, host, port, db)

    def get_cache(
        self,
    ) -> AsyncMemoryCache | SyncMemoryCache | AsyncRedisCache | SyncRedisCache | None:
        """Get the cache instance.

        Returns
        -------
            AsyncMemoryCache | SyncMemoryCache | AsyncRedisCache | SyncRedisCache | None: The current cache instance.

        """
        return self._cache

    def enable_unsafe_cache(self) -> None:
        """Enable unsafe cache mode."""
        self._unsafe_cache = True

    def disable_unsafe_cache(self) -> None:
        """Disable unsafe cache mode."""
        self._unsafe_cache = False

    def is_unsafe_cache_enabled(self) -> bool:
        """Check if unsafe cache mode is enabled.

        Returns
        -------
            bool: True if unsafe cache mode is enabled, otherwise False.

        """
        return self._unsafe_cache


# Singleton instance of CacheConfig
cache_config = CacheConfig()
