from enum import Enum

from pydantic import BaseModel, Field


class TransferDirection(str, Enum):
    """Enum for direction of transfer.

    `FUND_SFUTURES`: Funding Account->Standard Contract
    `SFUTURES_FUND`: Standard Contract->Funding Account
    `FUND_PFUTURES`: Funding Account->Perpetual Futures
    `PFUTURES_FUND`: Perpetual Futures->Funding Account
    `SFUTURES_PFUTURES`: Standard Contract->Perpetual Futures
    `PFUTURES_SFUTURES`: Perpetual Futures->Standard Contract
    """

    FUND_SFUTURES = "FUND_SFUTURES"
    SFUTURES_FUND = "SFUTURES_FUND"
    FUND_PFUTURES = "FUND_PFUTURES"
    PFUTURES_FUND = "PFUTURES_FUND"
    SFUTURES_PFUTURES = "SFUTURES_PFUTURES"
    PFUTURES_SFUTURES = "PFUTURES_SFUTURES"


class AssetBalance(BaseModel):
    """Model for asset balance data.

    Args:
        asset (str): Asset symbol (e.g., USDT, CHEEMS).
        free (str): Available balance.
        locked (str): Locked balance.

    """

    asset: str = Field(..., description="Asset symbol (e.g., USDT, CHEEMS)")
    free: str = Field(..., description="Available balance")
    locked: str = Field(..., description="Locked balance")


class QueryAssetsResponseData(BaseModel):
    """Model for the data field in QueryAssetsResponse.

    Args:
        balances (List[AssetBalance]): Asset list.

    """

    balances: list[AssetBalance] = Field(..., description="Asset list")


class QueryAssetsResponse(BaseModel):
    """Model for the response of Query Assets.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error Details Description.
        debug_msg (str): Debug message.
        data (QueryAssetsResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    debug_msg: str = Field(..., description="Debug message", alias="debugMsg")
    data: QueryAssetsResponseData = Field(..., description="Response data")


class AssetTransferResponse(BaseModel):
    """Model for the response of Asset Transfer.

    Args:
        tran_id (str): Transaction ID.

    """

    tran_id: str = Field(..., description="Transaction ID", alias="tranId")


class AssetTransferRecord(BaseModel):
    """Model for a single asset transfer record.

    Args:
        asset (str): Coin name.
        amount (str): Coin amount.
        type (str): Transfer type.
        status (str): Status, e.g., CONFIRMED.
        tran_id (int): Transaction ID.
        timestamp (int): Transfer timestamp.

    """

    asset: str = Field(..., description="Coin name")
    amount: str = Field(..., description="Coin amount")
    type: str = Field(..., description="Transfer type")
    status: str = Field(..., description="Status, e.g., CONFIRMED")
    tran_id: int = Field(..., description="Transaction ID", alias="tranId")
    timestamp: int = Field(..., description="Transfer timestamp")


class AssetTransferRecordsResponse(BaseModel):
    """Model for the response of Asset Transfer Records.

    Args:
        total (int): Total number of records.
        rows (List[AssetTransferRecord]): List of asset transfer records.

    """

    total: int = Field(..., description="Total number of records")
    rows: list[AssetTransferRecord] = Field(
        ...,
        description="List of asset transfer records",
    )


class InternalTransferRecord(BaseModel):
    """Model for a single internal transfer record.

    Args:
        id (int): Inner transfer ID.
        coin (str): Coin name.
        receiver (int): Receiver UID.
        amount (float): Transfer amount.
        status (int): Status (4=Pending review, 5=Failed, 6=Completed).
        from_uid (int): Payer's account.
        record_type (str): Record type (out: transfer out record, in: transfer in record).

    """

    id: int = Field(..., description="Inner transfer ID")
    coin: str = Field(..., description="Coin name")
    receiver: int = Field(..., description="Receiver UID")
    amount: float = Field(..., description="Transfer amount")
    status: int = Field(
        ...,
        description="Status (4=Pending review, 5=Failed, 6=Completed)",
    )
    from_uid: int = Field(..., description="Payer's account", alias="fromUid")
    record_type: str = Field(
        ...,
        description="Record type (out: transfer out record, in: transfer in record)",
        alias="recordType",
    )


class MainAccountInternalTransferRecordsResponseData(BaseModel):
    """Model for the data field in MainAccountInternalTransferRecordsResponse.

    Args:
        data (List[InternalTransferRecord]): Inner transfer records list.
        total (int): Total number of records.

    """

    data: list[InternalTransferRecord] = Field(
        ...,
        description="Inner transfer records list",
    )
    total: int = Field(..., description="Total number of records")


class MainAccountInternalTransferRecordsResponse(BaseModel):
    """Model for the response of Main Account Internal Transfer Records.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (MainAccountInternalTransferRecordsResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: MainAccountInternalTransferRecordsResponseData = Field(
        ...,
        description="Response data",
    )


class AccountType(str, Enum):
    """Enum for account types.

    Values:
        SPOT: Spot (fund account).
        STD_FUTURES: Standard futures account.
        COIN_M_PERP: Coin base account.
        USDT_M_PERP: U base account.
        COPY_TRADING: Copy trading account.
        GRID: Grid account.
        ERAN: Wealth account.
        C2C: C2C account.
    """

    SPOT = "sopt"
    STD_FUTURES = "stdFutures"
    COIN_M_PERP = "coinMPerp"
    USDT_M_PERP = "USDTMPerp"
    COPY_TRADING = "copyTrading"
    GRID = "grid"
    ERAN = "eran"
    C2C = "c2c"


class AssetOverviewResult(BaseModel):
    """Model for a single asset overview result.

    Args:
        account_type (AccountType): Account type.
        usdt_balance (str): Equivalent to USDT amount.

    """

    account_type: AccountType = Field(
        ...,
        description="Account type",
        alias="accountType",
    )
    usdt_balance: str = Field(
        ...,
        description="Equivalent to USDT amount",
        alias="usdtBalance",
    )


class AssetOverviewResponse(BaseModel):
    """Model for the response of Asset Overview.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (AssetOverviewResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list["AssetOverviewResult"] = Field(..., description="Response data")
