from pydantic import BaseModel, Field


class DepositRecord(BaseModel):
    """Model for a single deposit record.

    Args:
        amount (str): Recharge amount.
        coin (str): Coin name.
        network (str): Recharge network.
        status (int): Status (0-In progress, 6-Chain uploaded, 1-Completed).
        address (str): Recharge address.
        address_tag (str): Remark.
        tx_id (str): Transaction ID.
        insert_time (int): Transaction time.
        unlock_confirm (str): Confirm times for unlocking.
        confirm_times (str): Network confirmation times.

    """

    amount: str = Field(..., description="Recharge amount")
    coin: str = Field(..., description="Coin name")
    network: str = Field(..., description="Recharge network")
    status: int = Field(
        ...,
        description="Status (0-In progress, 6-Chain uploaded, 1-Completed)",
    )
    address: str = Field(..., description="Recharge address")
    address_tag: str = Field(..., description="Remark", alias="addressTag")
    tx_id: str = Field(..., description="Transaction ID", alias="txId")
    insert_time: int = Field(..., description="Transaction time", alias="insertTime")
    unlock_confirm: str = Field(
        ...,
        description="Confirm times for unlocking",
        alias="unlockConfirm",
    )
    confirm_times: str = Field(
        ...,
        description="Network confirmation times",
        alias="confirmTimes",
    )


class DepositRecordsResponse(BaseModel):
    """Model for the response of deposit records.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error message.
        data (List[DepositRecord]): List of deposit records.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error message")
    data: list[DepositRecord] = Field(..., description="List of deposit records")


class WithdrawRecord(BaseModel):
    """Model for a single withdraw record.

    Args:
        address (str): Withdrawal address.
        amount (str): Withdrawal amount.
        apply_time (str): Withdraw time.
        coin (str): Coin name.
        id (str): The ID of the withdrawal.
        network (str): Withdrawal network.
        transfer_type (int): Transfer type (1=Withdrawal, 2=Internal transfer).
        transaction_fee (str): Handling fee.
        confirm_no (int): Withdrawal confirmation times.
        info (str): Reason for withdrawal failure.
        tx_id (str): Withdrawal transaction ID.

    """

    address: str = Field(..., description="Withdrawal address")
    amount: str = Field(..., description="Withdrawal amount")
    apply_time: str = Field(..., description="Withdraw time", alias="applyTime")
    coin: str = Field(..., description="Coin name")
    id: str = Field(..., description="The ID of the withdrawal")
    network: str = Field(..., description="Withdrawal network")
    transfer_type: int = Field(
        ...,
        description="Transfer type (1=Withdrawal, 2=Internal transfer)",
        alias="transferType",
    )
    transaction_fee: str = Field(
        ...,
        description="Handling fee",
        alias="transactionFee",
    )
    confirm_no: int = Field(
        ...,
        description="Withdrawal confirmation times",
        alias="confirmNo",
    )
    info: str = Field(..., description="Reason for withdrawal failure")
    tx_id: str = Field(..., description="Withdrawal transaction ID", alias="txId")


class WithdrawRecordsResponse(BaseModel):
    """Model for the response of withdraw records.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error message.
        data (List[WithdrawRecord]): List of withdraw records.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error message")
    data: list[WithdrawRecord] = Field(..., description="List of withdraw records")


class NetworkInfo(BaseModel):
    """Model for network information.

    Args:
        name (str): Network name.
        network (str): Network identifier.
        is_default (bool): Whether it is the default network.
        min_confirm (int): Minimum confirmations required.
        withdraw_enable (bool): Whether withdrawals are enabled.
        deposit_enable (bool): Whether deposits are enabled.
        withdraw_fee (str): Withdrawal fee.
        withdraw_max (str): Maximum withdrawal amount.
        withdraw_min (str): Minimum withdrawal amount.
        deposit_min (str): Minimum deposit amount.

    """

    name: str = Field(..., description="Network name")
    network: str = Field(..., description="Network identifier")
    is_default: bool = Field(
        ...,
        description="Whether it is the default network",
        alias="isDefault",
    )
    min_confirm: int = Field(
        ...,
        description="Minimum confirmations required",
        alias="minConfirm",
    )
    withdraw_enable: bool = Field(
        ...,
        description="Whether withdrawals are enabled",
        alias="withdrawEnable",
    )
    deposit_enable: bool = Field(
        ...,
        description="Whether deposits are enabled",
        alias="depositEnable",
    )
    withdraw_fee: str = Field(..., description="Withdrawal fee", alias="withdrawFee")
    withdraw_max: str = Field(
        ...,
        description="Maximum withdrawal amount",
        alias="withdrawMax",
    )
    withdraw_min: str = Field(
        ...,
        description="Minimum withdrawal amount",
        alias="withdrawMin",
    )
    deposit_min: str = Field(
        ...,
        description="Minimum deposit amount",
        alias="depositMin",
    )


class CurrencyDepositWithdrawalDataResponse(BaseModel):
    """Model for the response of currency deposit and withdrawal data.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[CurrencyDepositWithdrawalData]): List of currency deposit and withdrawal data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list["CurrencyDepositWithdrawalData"] = Field(
        ...,
        description="List of currency deposit and withdrawal data",
    )


class CurrencyDepositWithdrawalData(BaseModel):
    """Model for currency deposit and withdrawal data.

    Args:
        coin (str): Coin identification.
        name (str): Coin name.
        network_list (List[NetworkInfo]): List of network information.

    """

    coin: str = Field(..., description="Coin identification")
    name: str = Field(..., description="Coin name")
    network_list: list[NetworkInfo] = Field(
        ...,
        description="List of network information",
        alias="networkList",
    )


class WithdrawResponse(BaseModel):
    """Model for the response of a withdrawal.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (WithdrawResponseData): Withdrawal response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: "WithdrawResponseData" = Field(..., description="Withdrawal response data")


class WithdrawResponseData(BaseModel):
    """Model for the data field in WithdrawResponse.

    Args:
        id (str): The platform returns the unique ID of the internal transfer record.

    """

    id: str = Field(
        ...,
        description="The platform returns the unique ID of the internal transfer record",
    )


class MainAccountDepositAddressResponse(BaseModel):
    """Model for the response of main account deposit address.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (MainAccountDepositAddressResponseData): Deposit address data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: "MainAccountDepositAddressResponseData" = Field(
        ...,
        description="Deposit address data",
    )


class MainAccountDepositAddressResponseData(BaseModel):
    """Model for the data field in MainAccountDepositAddressResponse.

    Args:
        data (List[DepositAddress]): List of deposit addresses.
        total (int): Total number of addresses.

    """

    data: list["DepositAddress"] = Field(..., description="List of deposit addresses")
    total: int = Field(..., description="Total number of addresses")


class DepositAddress(BaseModel):
    """Model for a single deposit address.

    Args:
        coin_id (int): Coin ID.
        coin (str): Coin name.
        network (str): Network name.
        address (str): Deposit address.
        tag (str): Address tag.

    """

    coin_id: int = Field(..., description="Coin ID", alias="coinId")
    coin: str = Field(..., description="Coin name")
    network: str = Field(..., description="Network name")
    address: str = Field(..., description="Deposit address")
    tag: str = Field(..., description="Address tag")


class DepositRiskControlRecord(BaseModel):
    """Model for a single deposit risk control record.

    Args:
        uid (str): User ID.
        coin (str): Currency name.
        amount (str): Amount.
        source_address (str): Source address.
        address (str): Recharge address.
        inset_time (str): Creation time.

    """

    uid: str = Field(..., description="User ID")
    coin: str = Field(..., description="Currency name")
    amount: str = Field(..., description="Amount")
    source_address: str = Field(
        ...,
        description="Source address",
        alias="sourceAddress",
    )
    address: str = Field(..., description="Recharge address")
    inset_time: str = Field(..., description="Creation time", alias="insetTime")


class DepositRiskControlRecordsResponse(BaseModel):
    """Model for the response of deposit risk control records.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error message.
        data (List[DepositRiskControlRecord]): List of deposit risk control records.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error message")
    data: list[DepositRiskControlRecord] = Field(
        ...,
        description="List of deposit risk control records",
    )
