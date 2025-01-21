"""Synchronous client for interacting with the BingX API.

This module provides a high-level client for interacting with the BingX API,
including support for spot trading, swap perpetual contracts, standard futures,
sub-accounts, and agent functionality. It also includes utilities for managing
API keys, listen keys for user data streams, and caching mechanisms for improved
performance.

The `BingXClient` class is the main entry point for interacting with the API.
It initializes sub-clients for specific functionalities like spot trading,
swap perpetual contracts, and more. Additionally, it provides methods for
managing user data streams and querying API key permissions and restrictions.

.. code-block:: python

    # Initialize the client
    client = BingXClient(api_key="your_api_key", api_secret="your_api_secret")

    # Generate a listen key for user data stream
    listen_key_response = client.generate_listen_key()
    print(listen_key_response)

    # Query API key permissions
    permissions = client.query_api_key_permissions()
    print(permissions)

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

from typing import Any, Optional

from bingx_py.caching import BaseCache
from bingx_py.client.agent import AgentAPI
from bingx_py.client.spot import SpotAPI
from bingx_py.client.standard import StandardFuturesAPI
from bingx_py.client.sub_account import SubAccountAPI
from bingx_py.client.swap import SwapPerpetualAPI
from bingx_py.http_client import BingXHttpClient
from bingx_py.models import (
    GenerateListenKeyResponse,
    QueryApiKeyPermissionsResponse,
    QueryApiKeyRestrictionsResponse,
)
from bingx_py.models.general import MainAccountInternalTransferResponse


class BingXClient(BingXHttpClient):
    """Client for interacting with the BingX API."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        demo_trading: bool = False,
        cache: Optional[BaseCache] = None,
        default_cache_ttl: int = 300,
    ) -> None:
        """Initialize the BingXClient.

        Args:
            api_key (str): The API key for authentication.
            api_secret (str): The API secret for signing requests.
            demo_trading (bool): Whether to use the demo trading environment. Defaults to False.
            cache (Optional[BaseCache]): The cache instance to use. Defaults to None.
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

    def generate_listen_key(self) -> GenerateListenKeyResponse:
        """Generate a listen key for user data stream.

        Returns
        -------
            GenerateListenKeyResponse: The response data.

        """
        return self.save_convert(
            self.post("/openApi/user/auth/userDataStream"),
            GenerateListenKeyResponse,
        )

    def extend_listen_key_validity(self, listen_key: str) -> None:
        """Extend the validity period of a listen key.

        Args:
            listen_key (str): The listen key to extend.

        Returns:
            None

        """
        params = {
            "listenKey": listen_key,
        }
        self.put("/openApi/user/auth/userDataStream", params=params)

    def delete_listen_key(self, listen_key: str) -> None:
        """Delete a listen key.

        Args:
            listen_key (str): The listen key to delete.

        Returns:
            None

        """
        params = {
            "listenKey": listen_key,
        }
        self.delete("/openApi/user/auth/userDataStream", params=params)

    def query_api_key_restrictions(
        self,
        recv_window: Optional[int] = None,
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
            self.get("/openApi/v1/account/apiRestrictions", params=params),
            QueryApiKeyRestrictionsResponse,
        )

    def query_api_key_permissions(
        self,
        recv_window: Optional[int] = None,
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
            self.get("/openApi/v1/account/apiPermissions", params=params),
            QueryApiKeyPermissionsResponse,
        )

    def main_account_internal_transfer(
        self,
        coin: str,
        user_account_type: int,
        user_account: str,
        amount: float,
        wallet_type: int,
        calling_code: Optional[str] = None,
        transfer_client_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> MainAccountInternalTransferResponse:
        """Perform an internal transfer within the main account.

        Args:
            coin (str): Name of the transferred currency.
            user_account_type (int): User account type (1=UID, 2=phone number, 3=email).
            user_account (str): User account (UID, phone number, email).
            amount (float): Transfer amount.
            wallet_type (int): Account type (1=Fund Account, 2=Standard Futures Account, 3=Perpetual Futures Account).
            calling_code (Optional[str]): Area code for telephone, required when userAccountType=2. Defaults to None.
            transfer_client_id (Optional[str]): Custom ID for internal transfer by the client. Defaults to None.
            recv_window (Optional[int]): Request validity time window, in milliseconds. Defaults to None.

        Returns:
            MainAccountInternalTransferResponse: The response data.

        """
        params: dict[str, Any] = {
            "coin": coin,
            "userAccountType": user_account_type,
            "userAccount": user_account,
            "amount": amount,
            "walletType": wallet_type,
        }
        if calling_code is not None:
            params["callingCode"] = calling_code
        if transfer_client_id is not None:
            params["transferClientId"] = transfer_client_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.save_convert(
            self.post(
                "/openApi/wallets/v1/capital/innerTransfer/apply",
                params=params,
            ),
            MainAccountInternalTransferResponse,
        )
