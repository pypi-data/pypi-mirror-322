"""Caching Module for BingX API.

This module provides synchronous and asynchronous caching implementations for the BingX API.
It includes in-memory and Redis-based caches, with support for time-to-live (TTL) and thread-safe operations.

Classes:
    - BaseCache: Abstract base class for synchronous caches.
    - BaseAsyncCache: Abstract base class for asynchronous caches.
    - SyncMemoryCache: Synchronous in-memory cache implementation.
    - AsyncMemoryCache: Asynchronous in-memory cache implementation.
    - SyncRedisCache: Synchronous Redis cache implementation.
    - AsyncRedisCache: Asynchronous Redis cache implementation.

.. code-block:: python

    from bingx_py.caching import SyncMemoryCache, AsyncMemoryCache

    # Synchronous in-memory cache
    sync_cache = SyncMemoryCache()
    sync_cache.set("key", {"data": "value"}, ttl=60)
    data = sync_cache.get("key")

    # Asynchronous in-memory cache
    async_cache = AsyncMemoryCache()
    await async_cache.aset("key", {"data": "value"}, ttl=60)
    data = await async_cache.aget("key")


"""

from .base import BaseAsyncCache, BaseCache
from .memory_cache import AsyncMemoryCache, SyncMemoryCache
from .redis_cache import AsyncRedisCache, SyncRedisCache

__all__ = [
    "AsyncMemoryCache",
    "AsyncRedisCache",
    "BaseAsyncCache",
    "BaseCache",
    "SyncMemoryCache",
    "SyncRedisCache",
]
