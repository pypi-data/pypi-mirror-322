from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.standard import (
    HistoricalOrderResponse,
    PositionsResponse,
    StandardContractBalanceResponse,
)

if TYPE_CHECKING:
    from bingx_py.asyncio import BingXHttpClient


class StandardFuturesAPI:
    """API for managing standard futures on BingX.

    This class provides methods to interact with standard futures features such
    as querying positions, placing orders, and more.
    """

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the StandardFuturesAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    async def get_all_positions(self) -> PositionsResponse:
        """Get all positions.

        Returns:
            PositionResponse: List of position data.

        """
        return self.client.save_convert(
            await self.client.async_get("/openApi/contract/v1/allPosition"),
            PositionsResponse,
        )

    async def get_historical_orders(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> HistoricalOrderResponse:
        """Get historical orders.

        Args:
            symbol (str): Currency pair, the format is similar: BTC-USDT, must pass.
            order_id (Optional[int]): Order ID, optional. Defaults to None.
            start_time (Optional[int]): Start time, optional. Defaults to None.
            end_time (Optional[int]): End time, optional. Defaults to None.
            limit (Optional[int]): Quantity, optional. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            HistoricalOrderResponse: List of historical order data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/contract/v1/allOrders",
                params=params,
            ),
            HistoricalOrderResponse,
        )

    async def query_standard_contract_balance(self) -> StandardContractBalanceResponse:
        """Query standard contract balance.

        Returns:
            StandardContractBalanceResponse: The response data.

        """
        return self.client.save_convert(
            await self.client.async_get("/openApi/contract/v1/balance"),
            StandardContractBalanceResponse,
        )
