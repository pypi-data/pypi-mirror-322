from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.spot.wallet import (
    CurrencyDepositWithdrawalDataResponse,
    DepositRecordsResponse,
    DepositRiskControlRecordsResponse,
    MainAccountDepositAddressResponse,
    WithdrawRecordsResponse,
    WithdrawResponse,
)

if TYPE_CHECKING:
    from bingx_py.client import BingXHttpClient


class WalletAPI:
    """API for managing wallet on BingX."""

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the WalletAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    def get_deposit_records(
        self,
        coin: Optional[str] = None,
        status: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> DepositRecordsResponse:
        """Get deposit records.

        Args:
            coin (Optional[str]): Coin name. Defaults to None.
            status (Optional[int]): Status (0-In progress, 6-Chain uploaded, 1-Completed). Defaults to None.
            start_time (Optional[int]): Start time in milliseconds. Defaults to None.
            end_time (Optional[int]): End time in milliseconds. Defaults to None.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 1000, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            DepositRecordsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if coin is not None:
            params["coin"] = coin
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
            self.client.get("/openApi/api/v3/capital/deposit/hisrec", params=params),
            DepositRecordsResponse,
        )

    def get_withdraw_records(
        self,
        withdraw_id: Optional[str] = None,
        coin: Optional[str] = None,
        withdraw_order_id: Optional[str] = None,
        status: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> WithdrawRecordsResponse:
        """Get withdraw records.

        Args:
            withdraw_id (Optional[str]): Unique ID of the withdrawal record. Defaults to None.
            coin (Optional[str]): Coin name. Defaults to None.
            withdraw_order_id (Optional[str]): Custom withdrawal ID. Defaults to None.
            status (Optional[int]): Status (4-Under Review, 5-Failed, 6-Completed). Defaults to None.
            start_time (Optional[int]): Start time in milliseconds. Defaults to None.
            end_time (Optional[int]): End time in milliseconds. Defaults to None.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 1000, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            WithdrawRecordsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if withdraw_id is not None:
            params["id"] = withdraw_id
        if coin is not None:
            params["coin"] = coin
        if withdraw_order_id is not None:
            params["withdrawOrderId"] = withdraw_order_id
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
            self.client.get("/openApi/api/v3/capital/withdraw/history", params=params),
            WithdrawRecordsResponse,
        )

    def get_currency_deposit_withdrawal_data(
        self,
        coin: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> CurrencyDepositWithdrawalDataResponse:
        """Get currency deposit and withdrawal data.

        Args:
            coin (Optional[str]): Coin identification. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            CurrencyDepositWithdrawalDataResponse: The response data.

        """
        params: dict[str, Any] = {}
        if coin is not None:
            params["coin"] = coin
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/wallets/v1/capital/config/getall", params=params),
            CurrencyDepositWithdrawalDataResponse,
        )

    def withdraw(
        self,
        coin: str,
        address: str,
        amount: float,
        wallet_type: int,
        network: Optional[str] = None,
        address_tag: Optional[str] = None,
        withdraw_order_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> WithdrawResponse:
        """Perform a withdrawal.

        Args:
            coin (str): Coin name.
            address (str): Withdrawal address.
            amount (float): Withdrawal amount.
            wallet_type (int): Account type (1=Fund Account, 2=Standard Account, 3=Perpetual Account).
            network (Optional[str]): Network name. Defaults to None.
            address_tag (Optional[str]): Tag or memo. Defaults to None.
            withdraw_order_id (Optional[str]): Custom withdrawal ID. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            WithdrawResponse: The response data.

        """
        params: dict[str, Any] = {
            "coin": coin,
            "address": address,
            "amount": amount,
            "walletType": wallet_type,
        }
        if network is not None:
            params["network"] = network
        if address_tag is not None:
            params["addressTag"] = address_tag
        if withdraw_order_id is not None:
            params["withdrawOrderId"] = withdraw_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post(
                "/openApi/wallets/v1/capital/withdraw/apply",
                params=params,
            ),
            WithdrawResponse,
        )

    def get_main_account_deposit_address(
        self,
        coin: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> MainAccountDepositAddressResponse:
        """Get main account deposit address.

        Args:
            coin (str): Name of the coin for transfer.
            offset (Optional[int]): Starting record number, default is 0. Defaults to None.
            limit (Optional[int]): Page size, default is 100, maximum is 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            MainAccountDepositAddressResponse: The response data.

        """
        params: dict[str, Any] = {
            "coin": coin,
        }
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get(
                "/openApi/wallets/v1/capital/deposit/address",
                params=params,
            ),
            MainAccountDepositAddressResponse,
        )

    def get_deposit_risk_control_records(self) -> DepositRiskControlRecordsResponse:
        """Get deposit risk control records.

        Returns:
            DepositRiskControlRecordsResponse: The response data.

        """
        return self.client.save_convert(
            self.client.get("/openApi/wallets/v1/capital/deposit/riskRecords"),
            DepositRiskControlRecordsResponse,
        )
