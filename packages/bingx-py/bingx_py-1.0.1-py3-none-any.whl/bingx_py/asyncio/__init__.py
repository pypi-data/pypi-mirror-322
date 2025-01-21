"""BingX API Async Client.

This module provides a high-level asynchronous client for interacting with the BingX API,
including support for spot trading, swap perpetual contracts, standard futures,
sub-accounts, and agent functionality. It also includes utilities for managing
API keys, listen keys for user data streams, and caching mechanisms for improved
performance.

The `BingXAsyncClient` class is the main entry point for interacting with the API.
It initializes sub-clients for specific functionalities like spot trading,
swap perpetual contracts, and more. Additionally, it provides methods for
managing user data streams and querying API key permissions and restrictions.

.. code-block:: python

    # Initialize the client
    client = BingXAsyncClient(api_key="your_api_key", api_secret="your_api_secret")

    # Generate a listen key for user data stream
    listen_key_response = await client.generate_listen_key()
    print(listen_key_response)

    # Query API key permissions
    permissions = await client.query_api_key_permissions()
    print(permissions)

Classes:
    BingXAsyncClient: The main asynchronous client class for interacting with the BingX API.

Sub-Clients:
    - SpotAPI: Client for spot trading functionality.
    - SwapPerpetualAPI: Client for swap perpetual contracts.
    - StandardFuturesAPI: Client for standard futures trading.
    - SubAccountAPI: Client for managing sub-accounts.
    - AgentAPI: Client for agent-related functionality.

Caching:
    The client supports caching through the `BaseCache` interface, which can be
    customized to use different caching backends (e.g., in-memory, Redis).
    Caching is particularly useful for reducing API calls and improving performance.

Note:
    Ensure that your API key and secret are kept secure. Avoid hardcoding them
    in your source code and use environment variables or secure vaults instead.

"""

from __future__ import annotations
from typing import TYPE_CHECKING, Any

from bingx_py.asyncio.agent import AgentAPI
from bingx_py.asyncio.spot import SpotAPI
from bingx_py.asyncio.standard import StandardFuturesAPI
from bingx_py.asyncio.sub_account import SubAccountAPI
from bingx_py.asyncio.swap import SwapPerpetualAPI
from bingx_py.http_client import BingXHttpClient
from bingx_py.models import (
    GenerateListenKeyResponse,
    QueryApiKeyPermissionsResponse,
    QueryApiKeyRestrictionsResponse,
)

if TYPE_CHECKING:
    from bingx_py.caching import BaseCache
    from bingx_py.caching.base import BaseAsyncCache


class BingXAsyncClient(BingXHttpClient):
    """Asynchronous client for interacting with the BingX API."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        demo_trading: bool = False,
        cache: BaseCache | BaseAsyncCache | None = None,
        default_cache_ttl: int = 300,
    ) -> None:
        """Initialize the BingXAsyncClient.

        Args:
            api_key (str): The API key for authentication.
            api_secret (str): The API secret for signing requests.
            demo_trading (bool): Whether to use the demo trading environment. Defaults to False.
            cache (Optional[BaseCache | BaseAsyncCache]): The cache instance to use. Defaults to None.
            default_cache_ttl (int): The default time-to-live (TTL) for cached data in seconds. Defaults to 300.

        Returns:
            None

        """
        self.demo_trading = demo_trading
        base_url = (
            "https://open-api-vst.bingx.com"
            if demo_trading
            else "https://open-api.bingx.com"
        )

        self.spot = SpotAPI(self)
        self.swap = SwapPerpetualAPI(self)
        self.agent = AgentAPI(self)
        self.standard = StandardFuturesAPI(self)
        self.sub_account = SubAccountAPI(self)

        super().__init__(api_key, api_secret, base_url, cache, default_cache_ttl)

    async def generate_listen_key(self) -> GenerateListenKeyResponse:
        """Generate a listen key for user data stream.

        Returns
        -------
            GenerateListenKeyResponse: The response data.

        """
        return self.save_convert(
            await self.async_post("/openApi/user/auth/userDataStream"),
            GenerateListenKeyResponse,
        )

    async def extend_listen_key_validity(self, listen_key: str) -> None:
        """Extend the validity period of a listen key.

        Args:
            listen_key (str): The listen key to extend.

        Returns:
            None

        """
        params = {
            "listenKey": listen_key,
        }
        await self.async_put("/openApi/user/auth/userDataStream", params=params)

    async def delete_listen_key(self, listen_key: str) -> None:
        """Delete a listen key.

        Args:
            listen_key (str): The listen key to delete.

        Returns:
            None

        """
        params = {
            "listenKey": listen_key,
        }
        await self.async_delete("/openApi/user/auth/userDataStream", params=params)

    async def query_api_key_restrictions(
        self,
        recv_window: int | None = None,
    ) -> QueryApiKeyRestrictionsResponse:
        """Query user API key restrictions.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryApiKeyRestrictionsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.save_convert(
            await self.async_get("/openApi/v1/account/apiRestrictions", params=params),
            QueryApiKeyRestrictionsResponse,
        )

    async def query_api_key_permissions(
        self,
        recv_window: int | None = None,
    ) -> QueryApiKeyPermissionsResponse:
        """Query user API key permissions.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryApiKeyPermissionsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.save_convert(
            await self.async_get("/openApi/v1/account/apiPermissions", params=params),
            QueryApiKeyPermissionsResponse,
        )
