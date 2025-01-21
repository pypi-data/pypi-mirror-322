"""BingX API Client Package.

This package provides synchronous and asynchronous clients for interacting with the BingX API.
It includes support for spot trading, swap perpetual trading, and caching configurations.

Classes:
    - `BingXClient`: Synchronous client for interacting with the BingX API.
    - `BingXAsyncClient`: Asynchronous client for interacting with the BingX API.

Configurations:
    - `cache_config`: Global caching configuration for managing API response caching.

Example:
.. code-block:: python
    from bingx_py import BingXClient, BingXAsyncClient, cache_config

    # Synchronous client
    client = BingXClient(api_key="your_api_key", api_secret="your_api_secret")
    account_data = client.generate_listen_key()

    # Asynchronous client
    async_client = BingXAsyncClient(api_key="your_api_key", api_secret="your_api_secret")
    account_data = await async_client.generate_listen_key()

    # Configure caching
    cache_config.set_cache("sync-redis")

"""

from .asyncio import BingXAsyncClient
from .client import BingXClient
from .config import cache_config

__all__ = [
    "BingXAsyncClient",
    "BingXClient",
    "cache_config",
]
