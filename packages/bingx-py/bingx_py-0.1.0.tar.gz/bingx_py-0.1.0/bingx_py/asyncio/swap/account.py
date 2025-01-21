from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.swap.account import (
    GetAccountProfitAndLossFundFlowResponse,
    QueryAccountDataResponse,
    QueryPositionDataResponse,
    SwapQueryTradingCommissionRateResponse,
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

    async def query_account_data(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryAccountDataResponse:
        """Query account data.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryAccountDataResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/swap/v3/user/balance", params=params),
            QueryAccountDataResponse,
        )

    async def query_position_data(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryPositionDataResponse:
        """Query position data.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryPositionDataResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/swap/v2/user/positions",
                params=params,
            ),
            QueryPositionDataResponse,
        )

    async def get_account_profit_and_loss_fund_flow(
        self,
        symbol: Optional[str] = None,
        income_type: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> GetAccountProfitAndLossFundFlowResponse:
        """Get account profit and loss fund flow.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            income_type (Optional[str]): Income type. Defaults to None.
            start_time (Optional[int]): Start time, timestamp in milliseconds. Defaults to None.
            end_time (Optional[int]): End time, timestamp in milliseconds. Defaults to None.
            limit (Optional[int]): Number of result sets to return. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            GetAccountProfitAndLossFundFlowResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if income_type is not None:
            params["incomeType"] = income_type
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/swap/v2/user/income", params=params),
            GetAccountProfitAndLossFundFlowResponse,
        )

    async def query_trading_commission_rate(
        self,
        recv_window: Optional[int] = None,
    ) -> SwapQueryTradingCommissionRateResponse:
        """Query trading commission rate.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SwapQueryTradingCommissionRateResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/swap/v2/user/commissionRate",
                params=params,
            ),
            SwapQueryTradingCommissionRateResponse,
        )
