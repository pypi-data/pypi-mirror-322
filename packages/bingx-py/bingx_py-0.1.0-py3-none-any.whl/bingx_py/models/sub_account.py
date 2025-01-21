from typing import Any, Optional

from pydantic import BaseModel, Field


class CreateSubAccountResponse(BaseModel):
    """Model for the response of CreateSubAccount.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (CreateSubAccountData): The response data.

    """

    code: int
    timestamp: int
    data: "CreateSubAccountData"


class CreateSubAccountData(BaseModel):
    """Model for the response data of CreateSubAccount.

    Args:
        sub_uid (int): Sub account uid.
        sub_account_string (str): Sub account username.

    """

    sub_uid: int = Field(..., alias="subUid")
    sub_account_string: str = Field(..., alias="subAccountString")


class QueryAccountUidResponse(BaseModel):
    """Model for the response of QueryAccountUid.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (QueryAccountUidData): The response data.

    """

    code: int
    timestamp: int
    data: "QueryAccountUidData"


class QueryAccountUidData(BaseModel):
    """Model for the response data of QueryAccountUid.

    Args:
        uid (int): Account uid.

    """

    uid: int


class GetSubAccountListResponse(BaseModel):
    """Model for the response of GetSubAccountList.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (GetSubAccountListData): The response data.

    """

    code: int
    timestamp: int
    data: "GetSubAccountListData"


class GetSubAccountListData(BaseModel):
    """Model for the response data of GetSubAccountList.

    Args:
        result (List[SubAccountInfo]): List of sub-accounts.
        page_id (int): Page number.
        total (int): Total number of sub-accounts.

    """

    result: list["SubAccountInfo"]
    page_id: int = Field(..., alias="pageId")
    total: int


class SubAccountInfo(BaseModel):
    """Model for the sub-account information.

    Args:
        sub_uid (int): Sub account uid.
        sub_account_string (str): Sub account username.
        note (str): Sub account note information.
        freeze (bool): Whether the account is frozen.
        create_time (int): Creation time.

    """

    sub_uid: int = Field(..., alias="subUid")
    sub_account_string: str = Field(..., alias="subAccountString")
    note: str
    freeze: bool
    create_time: int = Field(..., alias="createTime")


class QuerySubAccountSpotAssetsResponse(BaseModel):
    """Model for the response of QuerySubAccountSpotAssets.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (QuerySubAccountSpotAssetsData): The response data.

    """

    code: int
    timestamp: int
    data: "QuerySubAccountSpotAssetsData"


class QuerySubAccountSpotAssetsData(BaseModel):
    """Model for the response data of QuerySubAccountSpotAssets.

    Args:
        balances (List[AssetBalance]): List of asset balances.

    """

    balances: list["AssetBalance"]


class AssetBalance(BaseModel):
    """Model for the asset balance.

    Args:
        asset (str): Asset name.
        free (float): Available limit.
        locked (float): Locked assets.

    """

    asset: str
    free: float
    locked: float


class CreateSubAccountApiKeyResponse(BaseModel):
    """Model for the response of CreateSubAccountApiKey.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (CreateSubAccountApiKeyData): The response data.

    """

    code: int
    timestamp: int
    data: "CreateSubAccountApiKeyData"


class CreateSubAccountApiKeyData(BaseModel):
    """Model for the response data of CreateSubAccountApiKey.

    Args:
        note (str): Notes.
        api_key (str): API Key.
        api_secret (str): API Secret.
        permissions (List[str]): Permissions.
        ip_addresses (List[str]): IP whitelist.

    """

    note: str
    api_key: str = Field(..., alias="apiKey")
    api_secret: str = Field(..., alias="apiSecret")
    permissions: list[str]
    ip_addresses: list[str] = Field(..., alias="ipAddresses")


class QuerySubAccountApiKeyResponse(BaseModel):
    """Model for the response of QuerySubAccountApiKey.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (QuerySubAccountApiKeyData): The response data.

    """

    code: int
    timestamp: int
    data: "QuerySubAccountApiKeyData"


class QuerySubAccountApiKeyData(BaseModel):
    """Model for the response data of QuerySubAccountApiKey.

    Args:
        api_infos (List[ApiInfo]): List of API Key information.

    """

    api_infos: list["ApiInfo"] = Field(..., alias="apiInfos")


class ApiInfo(BaseModel):
    """Model for the API Key information.

    Args:
        api_key (str): API Key.
        note (str): Notes.
        permissions (List[int]): Permissions.
        ip_addresses (List[str]): IP whitelist.
        status (int): Status.
        create_time (int): Creation time.
        update_time (int): Update time.

    """

    api_key: str = Field(..., alias="apiKey")
    note: str
    permissions: list[int]
    ip_addresses: list[str] = Field(..., alias="ipAddresses")
    status: int
    create_time: int = Field(..., alias="createTime")
    update_time: int = Field(..., alias="updateTime")


class ResetSubAccountApiKeyResponse(BaseModel):
    """Model for the response of ResetSubAccountApiKey.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (ResetSubAccountApiKeyData): The response data.

    """

    code: int
    timestamp: int
    data: "ResetSubAccountApiKeyData"


class ResetSubAccountApiKeyData(BaseModel):
    """Model for the response data of ResetSubAccountApiKey.

    Args:
        note (str): Notes.
        permissions (List[int]): Permissions.
        ip_addresses (List[str]): IP whitelist.

    """

    note: str
    permissions: list[int]
    ip_addresses: list[str] = Field(..., alias="ipAddresses")


class DeleteSubAccountApiKeyResponse(BaseModel):
    """Model for the response of DeleteSubAccountApiKey.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.

    """

    code: int
    timestamp: int


class FreezeUnfreezeSubAccountResponse(BaseModel):
    """Model for the response of FreezeUnfreezeSubAccount.

    Args:
        sub_uid (int): Sub account uid.
        freeze (Optional[bool]): Whether the account is frozen.

    """

    sub_uid: int = Field(..., alias="subUid")
    freeze: Optional[bool] = None


class AuthorizeSubAccountInternalTransferResponse(BaseModel):
    """Model for the response of AuthorizeSubAccountInternalTransfer.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (bool): The response data.

    """

    code: int
    timestamp: int
    data: bool


class SubAccountInternalTransferResponse(BaseModel):
    """Model for the response of SubAccountInternalTransfer.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (SubAccountInternalTransferData): The response data.

    """

    code: int
    timestamp: int
    data: "SubAccountInternalTransferData"


class SubAccountInternalTransferData(BaseModel):
    """Model for the response data of SubAccountInternalTransfer.

    Args:
        id (str): The platform returns the unique ID of the internal transfer record.

    """

    id: str


class CreateSubAccountDepositAddressResponse(BaseModel):
    """Model for the response of CreateSubAccountDepositAddress.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (CreateSubAccountDepositAddressData): The response data.

    """

    code: int
    timestamp: int
    data: "CreateSubAccountDepositAddressData"


class CreateSubAccountDepositAddressData(BaseModel):
    """Model for the response data of CreateSubAccountDepositAddress.

    Args:
        coin (str): Currency name.
        address (str): Deposit address.
        network (str): Network name.
        address_tag (str): Address tag.
        status (int): Address status (0=activated, 1=pending, 2=not applied).
        ts (int): Creation time in Unix timestamp format in milliseconds.

    """

    coin: str
    address: str
    network: str
    address_tag: str = Field(..., alias="addressTag")
    status: int
    ts: int


class GetSubAccountDepositAddressResponse(BaseModel):
    """Model for the response of GetSubAccountDepositAddress.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (GetSubAccountDepositAddressData): The response data.

    """

    code: int
    timestamp: int
    data: "GetSubAccountDepositAddressData"


class GetSubAccountDepositAddressData(BaseModel):
    """Model for the response data of GetSubAccountDepositAddress.

    Args:
        data (List[DepositAddress]): List of deposit addresses.
        total (int): Total number of addresses.

    """

    data: list["DepositAddress"]
    total: int


class DepositAddress(BaseModel):
    """Model for the deposit address.

    Args:
        coin (str): Coin name.
        network (str): Network name.
        address (str): Deposit address.
        address_with_prefix (str): Deposit address with prefix.
        tag (str): Address tag.
        status (int): Address status (0=activated, 1=applied, 2=not applied).

    """

    coin: str
    network: str
    address: str
    address_with_prefix: str = Field(..., alias="addressWithPrefix")
    tag: str
    status: int


class GetSubAccountDepositRecordsResponse(BaseModel):
    """Model for the response of GetSubAccountDepositRecords.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (GetSubAccountDepositRecordsData): The response data.

    """

    code: int
    timestamp: int
    data: "GetSubAccountDepositRecordsData"


class GetSubAccountDepositRecordsData(BaseModel):
    """Model for the response data of GetSubAccountDepositRecords.

    Args:
        total (int): Total number of records.
        data (List[DepositRecord]): List of deposit records.

    """

    total: int
    data: list["DepositRecord"]


class DepositRecord(BaseModel):
    """Model for a deposit record.

    Args:
        sub_uid (int): Sub-account UID.
        amount (float): Transfer amount.
        coin (str): Currency name.
        network (str): Network name.
        status (int): Status (0-In progress, 6-Chain uploaded, 1-Completed).
        address (str): Deposit address.
        address_tag (str): Deposit address tag.
        tx_id (str): Transaction ID.
        insert_time (int): Transaction scan time.
        transfer_type (int): Transfer type (0-deposit).
        unlock_confirm_times (int): Number of confirmations required to unlock the deposit.
        confirm_times (int): Number of confirmations.

    """

    sub_uid: int = Field(..., alias="subUid")
    amount: float
    coin: str
    network: str
    status: int
    address: str
    address_tag: str = Field(..., alias="addressTag")
    tx_id: str = Field(..., alias="txId")
    insert_time: int = Field(..., alias="insertTime")
    transfer_type: int = Field(..., alias="transferType")
    unlock_confirm_times: int = Field(..., alias="unlockConfirmTimes")
    confirm_times: int = Field(..., alias="confirmTimes")


class QuerySubAccountInternalTransferRecordsResponse(BaseModel):
    """Model for the response of QuerySubAccountInternalTransferRecords.

    Args:
        data (Optional[Dict[str, Any]]): Internal transfer record list.
        total (Optional[int]): Total number of records.
        id (int): Internal transfer ID.
        coin (str): Currency name.
        receiver (int): Receiver's UID.
        amount (float): Transfer amount.
        time (int): Internal transfer time.
        status (Optional[int]): Status (4-Pending review, 5-Failed, 6-Completed).
        transfer_client_id (str): Client's self-defined internal transfer ID.
        from_uid (int): Payer's account.
        record_type (str): Transfer type (out: transfer out, in: transfer in).

    """

    data: Optional[dict[str, Any]] = None
    total: Optional[int] = None
    id: int
    coin: str
    receiver: int
    amount: float
    time: int
    status: Optional[int] = None
    transfer_client_id: str = Field(..., alias="transferClientId")
    from_uid: int = Field(..., alias="fromUid")
    record_type: str = Field(..., alias="recordType")


class QuerySubAccountTransferHistoryResponse(BaseModel):
    """Model for the response of QuerySubAccountTransferHistory.

    Args:
        total (int): Total count.
        rows (List[TransferRecord]): Data array.

    """

    total: int
    rows: list["TransferRecord"]


class TransferRecord(BaseModel):
    """Model for a transfer record.

    Args:
        asset (str): Name of the asset.
        amount (float): Amount of the asset.
        type (str): Transfer type.
        status (str): Status (e.g., CONFIRMED).
        tran_id (str): Transfer ID.
        timestamp (int): Transfer timestamp.
        from_uid (int): UID of the sender.
        to_uid (int): UID of the receiver.

    """

    asset: str
    amount: float
    type: str
    status: str
    tran_id: str = Field(..., alias="tranId")
    timestamp: int
    from_uid: int = Field(..., alias="fromUid")
    to_uid: int = Field(..., alias="toUid")


class QueryTransferableAmountResponse(BaseModel):
    """Model for the response of QueryTransferableAmount.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (QueryTransferableAmountData): The response data.

    """

    code: int
    timestamp: int
    data: "QueryTransferableAmountData"


class QueryTransferableAmountData(BaseModel):
    """Model for the response data of QueryTransferableAmount.

    Args:
        coins (List[CoinInfo]): List of supported coins.

    """

    coins: list["CoinInfo"]


class CoinInfo(BaseModel):
    """Model for coin information.

    Args:
        id (int): Coin ID.
        name (str): Coin name, e.g., USDT.
        available_amount (float): Available transfer amount.

    """

    id: int
    name: str
    available_amount: float = Field(..., alias="availableAmount")


class SubAccountAssetTransferResponse(BaseModel):
    """Model for the response of SubAccountAssetTransfer.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (SubAccountAssetTransferData): The response data.

    """

    code: int
    timestamp: int
    data: "SubAccountAssetTransferData"


class SubAccountAssetTransferData(BaseModel):
    """Model for the response data of SubAccountAssetTransfer.

    Args:
        tran_id (str): Transfer record ID.

    """

    tran_id: str = Field(..., alias="tranId")


class BatchQuerySubAccountAssetOverviewResponse(BaseModel):
    """Model for the response of BatchQuerySubAccountAssetOverview.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        timestamp (int): Response timestamp.
        data (BatchQuerySubAccountAssetOverviewData): The response data.

    """

    code: int
    timestamp: int
    data: "BatchQuerySubAccountAssetOverviewData"


class BatchQuerySubAccountAssetOverviewData(BaseModel):
    """Model for the response data of BatchQuerySubAccountAssetOverview.

    Args:
        result (List[SubAccountAssetInfo]): List of sub-account asset information.
        page_id (int): Page number.
        total (int): Total number of records.

    """

    result: list["SubAccountAssetInfo"]
    page_id: int = Field(..., alias="pageId")
    total: int


class SubAccountAssetInfo(BaseModel):
    """Model for sub-account asset information.

    Args:
        sub_uid (int): Sub-account UID.
        account_balances (List[AccountBalance]): List of account balances.

    """

    sub_uid: int = Field(..., alias="subUid")
    account_balances: list["AccountBalance"] = Field(..., alias="accountBalances")


class AccountBalance(BaseModel):
    """Model for account balance.

    Args:
        account_type (str): Account type.
        usdt_balance (float): Equivalent to USDT amount.

    """

    account_type: str = Field(..., alias="accountType")
    usdt_balance: float = Field(..., alias="usdtBalance")
