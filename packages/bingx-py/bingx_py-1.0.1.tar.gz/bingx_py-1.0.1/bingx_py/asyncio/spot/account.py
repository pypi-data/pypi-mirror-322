from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.agent import PaginationParams
from bingx_py.models.spot.account import (
    AccountType,
    AssetOverviewResponse,
    AssetTransferRecordsResponse,
    AssetTransferResponse,
    MainAccountInternalTransferRecordsResponse,
    QueryAssetsResponse,
    TransferDirection,
)

if TYPE_CHECKING:
    from bingx_py.asyncio import BingXHttpClient


class AccountAPI:
    """API for managing account on BingX."""

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the AccountAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    async def query_assets(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryAssetsResponse:
        """Query assets.

        Args:
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            QueryAssetsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/spot/v1/account/balance",
                params=params,
            ),
            QueryAssetsResponse,
        )

    async def transfer_asset(
        self,
        transfer_type: TransferDirection,
        asset: str,
        amount: float,
        recv_window: Optional[int] = None,
    ) -> AssetTransferResponse:
        """Perform an asset transfer.

        Args:
            transfer_type (TransferDirection): Transfer type.
            asset (str): Coin name, e.g., USDT.
            amount (float): Amount to transfer.
            recv_window (Optional[int]): Execution window time, cannot be greater than 60000. Defaults to None.

        Returns:
            AssetTransferResponse: The response data.

        """
        params: dict[str, Any] = {
            "type": transfer_type,
            "asset": asset,
            "amount": amount,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/api/v3/post/asset/transfer",
                params=params,
            ),
            AssetTransferResponse,
        )

    async def get_transfer_asset_records(
        self,
        transfer_type: TransferDirection,
        tran_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        pagination: Optional[PaginationParams] = None,
        recv_window: Optional[int] = None,
    ) -> AssetTransferRecordsResponse:
        """Get asset transfer records.

        Args:
            transfer_type (TransferDirection): Transfer type, (query by type or tranId).
            tran_id (Optional[int]): Transaction ID, (query by type or tranId). Defaults to None.
            start_time (Optional[int]): Starting time. Defaults to None.
            end_time (Optional[int]): End time. Defaults to None.
            pagination (Optional[PaginationParams]): Pagination parameters. Defaults to None.
            recv_window (Optional[int]): Execution window time, cannot be greater than 60000. Defaults to None.

        Returns:
            AssetTransferRecordsResponse: The response data.

        """
        params: dict[str, Any] = {
            "type": transfer_type,
        }
        if tran_id is not None:
            params["tranId"] = tran_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if pagination is not None:
            params["current"] = pagination.page_index
            params["size"] = pagination.page_size
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/api/v3/asset/transfer",
                params=params,
            ),
            AssetTransferRecordsResponse,
        )

    async def get_main_account_internal_transfer_records(
        self,
        coin: str,
        transfer_client_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> MainAccountInternalTransferRecordsResponse:
        """Get main account internal transfer records.

        Args:
            coin (str): Transfer coin name.
            transfer_client_id (Optional[str]): Client's self-defined internal transfer ID. Defaults to None.
            start_time (Optional[int]): Start time. Defaults to None.
            end_time (Optional[int]): End time. Defaults to None.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 100, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window in milliseconds. Defaults to None.

        Returns:
            MainAccountInternalTransferRecordsResponse: The response data.

        """
        params: dict[str, Any] = {
            "coin": coin,
        }
        if transfer_client_id is not None:
            params["transferClientId"] = transfer_client_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/wallets/v1/capital/innerTransfer/records",
                params=params,
            ),
            MainAccountInternalTransferRecordsResponse,
        )

    async def get_asset_overview(
        self,
        account_type: Optional[AccountType] = None,
        recv_window: Optional[int] = None,
    ) -> AssetOverviewResponse:
        """Get asset overview.

        Args:
            account_type (Optional[AccountType]): Account type. If left blank, all assets of the account will be checked by default. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            AssetOverviewResponse` The response data.

        """
        params: dict[str, Any] = {}
        if account_type is not None:
            params["accountType"] = account_type.value
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/account/v1/allAccountBalance",
                params=params,
            ),
            AssetOverviewResponse,
        )
