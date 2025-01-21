from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.sub_account import (
    AuthorizeSubAccountInternalTransferResponse,
    BatchQuerySubAccountAssetOverviewResponse,
    CreateSubAccountApiKeyResponse,
    CreateSubAccountDepositAddressResponse,
    CreateSubAccountResponse,
    DeleteSubAccountApiKeyResponse,
    FreezeUnfreezeSubAccountResponse,
    GetSubAccountDepositAddressResponse,
    GetSubAccountDepositRecordsResponse,
    GetSubAccountListResponse,
    QueryAccountUidResponse,
    QuerySubAccountApiKeyResponse,
    QuerySubAccountInternalTransferRecordsResponse,
    QuerySubAccountSpotAssetsResponse,
    QuerySubAccountTransferHistoryResponse,
    QueryTransferableAmountResponse,
    ResetSubAccountApiKeyResponse,
    SubAccountAssetTransferResponse,
    SubAccountInternalTransferResponse,
)

if TYPE_CHECKING:
    from bingx_py.asyncio import BingXHttpClient


class SubAccountAPI:
    """API for managing sub-accounts on BingX.

    This class provides methods to create, manage, and query sub-accounts,
    including creating API keys, managing deposits, and transferring assets
    between sub-accounts and the main account.
    """

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the SubAccountAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    async def create_sub_account(
        self,
        sub_account_string: str,
        note: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> CreateSubAccountResponse:
        """Create a new sub-account.

        Args:
            sub_account_string (str): Sub account username (Starting with a letter, containing a number, and longer than 6 characters).
            note (Optional[str]): Notes. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            CreateSubAccountResponse: The response data.

        """
        params: dict[str, Any] = {
            "subAccountString": sub_account_string,
        }
        if note is not None:
            params["note"] = note
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/subAccount/v1/create",
                params=params,
            ),
            CreateSubAccountResponse,
        )

    async def query_account_uid(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryAccountUidResponse:
        """Query the account UID.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryAccountUidResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/account/v1/uid", params=params),
            QueryAccountUidResponse,
        )

    async def get_sub_account_list(
        self,
        page: int,
        limit: int,
        sub_uid: Optional[int] = None,
        sub_account_string: Optional[str] = None,
        is_freeze: Optional[bool] = None,
        recv_window: Optional[int] = None,
    ) -> GetSubAccountListResponse:
        """Get the list of sub-accounts.

        Args:
            page (int): Page number, starting with 1.
            limit (int): Paging size, maximum 1000.
            sub_uid (Optional[int]): Sub account uid. Defaults to None.
            sub_account_string (Optional[str]): Sub account username. Defaults to None.
            is_freeze (Optional[bool]): Freeze or not. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            GetSubAccountListResponse: The response data.

        """
        params: dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if sub_uid is not None:
            params["subUid"] = sub_uid
        if sub_account_string is not None:
            params["subAccountString"] = sub_account_string
        if is_freeze is not None:
            params["isFeeze"] = is_freeze
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/subAccount/v1/list", params=params),
            GetSubAccountListResponse,
        )

    async def query_sub_account_spot_assets(
        self,
        sub_uid: int,
        recv_window: Optional[int] = None,
    ) -> QuerySubAccountSpotAssetsResponse:
        """Query the spot assets of a sub-account.

        Args:
            sub_uid (int): Sub account uid.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QuerySubAccountSpotAssetsResponse: The response data.

        """
        params: dict[str, Any] = {
            "subUid": sub_uid,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/subAccount/v1/assets", params=params),
            QuerySubAccountSpotAssetsResponse,
        )

    async def create_sub_account_api_key(
        self,
        sub_uid: int,
        note: str,
        permissions: list[str],
        ip_addresses: Optional[list[str]] = None,
        recv_window: Optional[int] = None,
    ) -> CreateSubAccountApiKeyResponse:
        """Create an API Key for a sub-account.

        Args:
            sub_uid (int): Sub account uid.
            note (str): Notes.
            permissions (List[str]): Permissions, e.g., ["1", "2", "3"].
            ip_addresses (Optional[List[str]]): IP whitelist. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            CreateSubAccountApiKeyResponse: The response data.

        """
        params: dict[str, Any] = {
            "subUid": sub_uid,
            "note": note,
            "permissions": permissions,
        }
        if ip_addresses is not None:
            params["ipAddresses"] = ip_addresses
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/subAccount/v1/apiKey/create",
                params=params,
            ),
            CreateSubAccountApiKeyResponse,
        )

    async def query_sub_account_api_key(
        self,
        uid: int,
        api_key: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QuerySubAccountApiKeyResponse:
        """Query the API Key of a sub-account.

        Args:
            uid (int): User uid.
            api_key (Optional[str]): API Key. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QuerySubAccountApiKeyResponse: The response data.

        """
        params: dict[str, Any] = {
            "uid": uid,
        }
        if api_key is not None:
            params["apiKey"] = api_key
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/account/v1/apiKey/query",
                params=params,
            ),
            QuerySubAccountApiKeyResponse,
        )

    async def reset_sub_account_api_key(
        self,
        sub_uid: int,
        api_key: str,
        note: str,
        permissions: list[int],
        ip_addresses: Optional[list[str]] = None,
        recv_window: Optional[int] = None,
    ) -> ResetSubAccountApiKeyResponse:
        """Reset the API Key of a sub-account.

        Args:
            sub_uid (int): Sub account uid.
            api_key (str): API Key.
            note (str): Notes.
            permissions (List[int]): Permissions, e.g., [1, 2, 3].
            ip_addresses (Optional[List[str]]): IP whitelist. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            ResetSubAccountApiKeyResponse: The response data.

        """
        params: dict[str, Any] = {
            "subUid": sub_uid,
            "apiKey": api_key,
            "note": note,
            "permissions": permissions,
        }
        if ip_addresses is not None:
            params["ipAddresses"] = ip_addresses
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/subAccount/v1/apiKey/edit",
                params=params,
            ),
            ResetSubAccountApiKeyResponse,
        )

    async def delete_sub_account_api_key(
        self,
        sub_uid: int,
        api_key: str,
        recv_window: Optional[int] = None,
    ) -> DeleteSubAccountApiKeyResponse:
        """Delete the API Key of a sub-account.

        Args:
            sub_uid (int): Sub account uid.
            api_key (str): API Key.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            DeleteSubAccountApiKeyResponse: The response data.

        """
        params: dict[str, Any] = {
            "subUid": sub_uid,
            "apiKey": api_key,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/subAccount/v1/apiKey/del",
                params=params,
            ),
            DeleteSubAccountApiKeyResponse,
        )

    async def freeze_unfreeze_sub_account(
        self,
        sub_uid: int,
        freeze: bool,
        recv_window: Optional[int] = None,
    ) -> FreezeUnfreezeSubAccountResponse:
        """Freeze or unfreeze a sub-account.

        Args:
            sub_uid (int): Sub account uid.
            freeze (bool): Whether to freeze the account.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            FreezeUnfreezeSubAccountResponse: The response data.

        """
        params: dict[str, Any] = {
            "subUid": sub_uid,
            "freeze": freeze,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/subAccount/v1/updateStatus",
                params=params,
            ),
            FreezeUnfreezeSubAccountResponse,
        )

    async def authorize_sub_account_internal_transfer(
        self,
        sub_uids: str,
        transferable: bool,
        recv_window: Optional[int] = None,
    ) -> AuthorizeSubAccountInternalTransferResponse:
        """Authorize sub-account internal transfers.

        Args:
            sub_uids (str): User uid list, comma separated.
            transferable (bool): Is it allowed? True allows, false prohibits.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            AuthorizeSubAccountInternalTransferResponse: The response data.

        """
        params: dict[str, Any] = {
            "subUids": sub_uids,
            "transferable": transferable,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/account/v1/innerTransfer/authorizeSubAccount",
                params=params,
            ),
            AuthorizeSubAccountInternalTransferResponse,
        )

    async def sub_account_internal_transfer(
        self,
        coin: str,
        user_account_type: int,
        user_account: str,
        amount: float,
        wallet_type: int,
        calling_code: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> SubAccountInternalTransferResponse:
        """Perform an internal transfer within a sub-account.

        Args:
            coin (str): Transfer currency name.
            user_account_type (int): User account type (1=UID, 2=phone number, 3=email).
            user_account (str): User account (UID, phone, email).
            amount (float): Transfer amount.
            wallet_type (int): Account type (1=Fund Account, 2=Standard Futures Account, 3=Perpetual Futures Account).
            calling_code (Optional[str]): Area code for telephone, required when userAccountType=2. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            SubAccountInternalTransferResponse: The response data.

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
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/wallets/v1/capital/subAccountInnerTransfer/apply",
                params=params,
            ),
            SubAccountInternalTransferResponse,
        )

    async def create_sub_account_deposit_address(
        self,
        coin: str,
        sub_uid: int,
        network: str,
        wallet_type: int,
        recv_window: Optional[int] = None,
    ) -> CreateSubAccountDepositAddressResponse:
        """Create a deposit address for a sub-account.

        Args:
            coin (str): Currency name.
            sub_uid (int): Sub-account UID.
            network (str): Network name.
            wallet_type (int): Account type (1=Fund Account, 2=Standard Futures Account, 3=USDⓢ-M Perp).
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            CreateSubAccountDepositAddressResponse: The response data.

        """
        params: dict[str, Any] = {
            "coin": coin,
            "subUid": sub_uid,
            "network": network,
            "walletType": wallet_type,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/wallets/v1/capital/deposit/createSubAddress",
                params=params,
            ),
            CreateSubAccountDepositAddressResponse,
        )

    async def get_sub_account_deposit_address(
        self,
        coin: str,
        sub_uid: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> GetSubAccountDepositAddressResponse:
        """Get the deposit address for a sub-account.

        Args:
            coin (str): Name of the transfer coin.
            sub_uid (int): Sub-account UID.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 100, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            GetSubAccountDepositAddressResponse: The response data.

        """
        params: dict[str, Any] = {
            "coin": coin,
            "subUid": sub_uid,
        }
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/wallets/v1/capital/subAccount/deposit/address",
                params=params,
            ),
            GetSubAccountDepositAddressResponse,
        )

    async def get_sub_account_deposit_records(
        self,
        coin: Optional[str] = None,
        sub_uid: Optional[int] = None,
        status: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> GetSubAccountDepositRecordsResponse:
        """Get deposit records for sub-accounts.

        Args:
            coin (Optional[str]): Transfer currency name. Defaults to None.
            sub_uid (Optional[int]): Sub-account UID. Defaults to None.
            status (Optional[int]): Status (0-In progress, 6-Chain uploaded, 1-Completed). Defaults to None.
            start_time (Optional[int]): Start time. Defaults to None.
            end_time (Optional[int]): End time. Defaults to None.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 100, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            GetSubAccountDepositRecordsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if coin is not None:
            params["coin"] = coin
        if sub_uid is not None:
            params["subUid"] = sub_uid
        if status is not None:
            params["status"] = status
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
                "/openApi/wallets/v1/capital/deposit/subHisrec",
                params=params,
            ),
            GetSubAccountDepositRecordsResponse,
        )

    async def query_sub_account_internal_transfer_records(
        self,
        coin: str,
        transfer_client_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QuerySubAccountInternalTransferRecordsResponse:
        """Query internal transfer records for sub-accounts.

        Args:
            coin (str): Transfer currency name.
            transfer_client_id (Optional[str]): Client's self-defined internal transfer ID. Defaults to None.
            start_time (Optional[int]): Start time. Defaults to None.
            end_time (Optional[int]): End time. Defaults to None.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 100, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            QuerySubAccountInternalTransferRecordsResponse: The response data.

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
                "/openApi/wallets/v1/capital/subAccount/innerTransfer/records",
                params=params,
            ),
            QuerySubAccountInternalTransferRecordsResponse,
        )

    async def query_sub_account_transfer_history(
        self,
        uid: int,
        transfer_type: Optional[str] = None,
        tran_id: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page_id: Optional[int] = None,
        paging_size: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QuerySubAccountTransferHistoryResponse:
        """Query transfer history for sub-accounts (for master account operations only).

        Args:
            uid (int): UID to query.
            transfer_type (Optional[str]): Transfer type. Defaults to None.
            tran_id (Optional[str]): Transfer ID. Defaults to None.
            start_time (Optional[int]): Start time. Defaults to None.
            end_time (Optional[int]): End time. Defaults to None.
            page_id (Optional[int]): Current page, default is 1. Defaults to None.
            paging_size (Optional[int]): Page size, default is 10, cannot exceed 100. Defaults to None.
            recv_window (Optional[int]): Execution window time, cannot exceed 60000. Defaults to None.

        Returns:
            QuerySubAccountTransferHistoryResponse: The response data.

        """
        params: dict[str, Any] = {
            "uid": uid,
        }
        if transfer_type is not None:
            params["type"] = transfer_type
        if tran_id is not None:
            params["tranId"] = tran_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if page_id is not None:
            params["pageId"] = page_id
        if paging_size is not None:
            params["pagingSize"] = paging_size
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/account/transfer/v1/subAccount/asset/transferHistory",
                params=params,
            ),
            QuerySubAccountTransferHistoryResponse,
        )

    async def query_transferable_amount(
        self,
        from_uid: int,
        from_account_type: int,
        to_uid: int,
        to_account_type: int,
        recv_window: Optional[int] = None,
    ) -> QueryTransferableAmountResponse:
        """Query the transferable amount of funds in the parent-child account (only for parent account operations).

        Args:
            from_uid (int): Sender UID.
            from_account_type (int): Sender account type (1=Fund account, 2=Contract account, 3=Perpetual USD-based account).
            to_uid (int): Receiver UID.
            to_account_type (int): Receiver account type (1=Fund account, 2=Contract account, 3=Perpetual USD-based account).
            recv_window (Optional[int]): Execution window time, cannot exceed 60000. Defaults to None.

        Returns:
            QueryTransferableAmountResponse: The response data.

        """
        params: dict[str, Any] = {
            "fromUid": from_uid,
            "fromAccountType": from_account_type,
            "toUid": to_uid,
            "toAccountType": to_account_type,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/account/transfer/v1/subAccount/transferAsset/supportCoins",
                params=params,
            ),
            QueryTransferableAmountResponse,
        )

    async def sub_account_asset_transfer(
        self,
        asset_name: str,
        transfer_amount: float,
        from_uid: int,
        from_type: int,
        from_account_type: int,
        to_uid: int,
        to_type: int,
        to_account_type: int,
        remark: str,
        recv_window: Optional[int] = None,
    ) -> SubAccountAssetTransferResponse:
        """Perform asset transfer between sub-accounts (for master account operations only).

        Args:
            asset_name (str): Name of the asset, e.g., USDT.
            transfer_amount (float): Transfer amount.
            from_uid (int): Sender UID.
            from_type (int): Sender sub/master account type (1=Master account, 2=Sub-account).
            from_account_type (int): Sender account type (1=Fund account, 2=Contract account, 3=Perpetual USD-based account).
            to_uid (int): Receiver UID.
            to_type (int): Receiver sub/master account type (1=Master account, 2=Sub-account).
            to_account_type (int): Receiver account type (1=Fund account, 2=Contract account, 3=Perpetual USD-based account).
            remark (str): Transfer remark.
            recv_window (Optional[int]): Execution window time, cannot exceed 60000. Defaults to None.

        Returns:
            SubAccountAssetTransferResponse: The response data.

        """
        params: dict[str, Any] = {
            "assetName": asset_name,
            "transferAmount": transfer_amount,
            "fromUid": from_uid,
            "fromType": from_type,
            "fromAccountType": from_account_type,
            "toUid": to_uid,
            "toType": to_type,
            "toAccountType": to_account_type,
            "remark": remark,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_post(
                "/openApi/account/transfer/v1/subAccount/transferAsset",
                params=params,
            ),
            SubAccountAssetTransferResponse,
        )

    async def batch_query_sub_account_asset_overview(
        self,
        page_index: int,
        page_size: int,
        sub_uid: Optional[int] = None,
        account_type: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> BatchQuerySubAccountAssetOverviewResponse:
        """Batch query of sub-account asset overview.

        Args:
            page_index (int): Page number, must be greater than 0.
            page_size (int): Paging size, must be greater than 0, maximum 10.
            sub_uid (Optional[int]): Sub-account UID. Defaults to None.
            account_type (Optional[str]): Account type. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            BatchQuerySubAccountAssetOverviewResponse: The response data.

        """
        params: dict[str, Any] = {
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if sub_uid is not None:
            params["subUid"] = sub_uid
        if account_type is not None:
            params["accountType"] = account_type
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/subAccount/v1/allAccountBalance",
                params=params,
            ),
            BatchQuerySubAccountAssetOverviewResponse,
        )
