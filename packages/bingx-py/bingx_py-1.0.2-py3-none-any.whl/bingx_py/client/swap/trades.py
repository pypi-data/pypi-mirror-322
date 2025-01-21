from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.swap.trades import (
    ApplyVstResponse,
    BatchCancelReplaceOrdersResponse,
    CancelAllAfterResponse,
    CancelAllOpenOrdersResponse,
    CancelMultipleOrdersResponse,
    CancelOrderResponse,
    CancelReplaceOrderRequest,
    CancelReplaceOrderResponse,
    CancelTwapOrderResponse,
    ChangeMarginTypeResponse,
    CloseAllPositionsResponse,
    ClosePositionResponse,
    CurrentAllOpenOrdersResponse,
    HedgeModeAutoAddMarginResponse,
    IsolatedMarginChangeHistoryResponse,
    MarginType,
    ModifyIsolatedPositionMarginResponse,
    OneClickReversePositionResponse,
    OrderRequest,
    OrderType,
    PlaceMultipleOrdersResponse,
    PlaceOrderInDemoTradingResponse,
    PlaceOrderResponse,
    PlaceTwapOrderResponse,
    PositionAndMaintenanceMarginRatioResponse,
    QueryAllOrdersResponse,
    QueryHistoricalTransactionDetailsResponse,
    QueryHistoricalTransactionOrdersResponse,
    QueryLeverageAndAvailablePositionsResponse,
    QueryMarginTypeResponse,
    QueryMultiAssetsMarginResponse,
    QueryMultiAssetsModeResponse,
    QueryMultiAssetsRulesResponse,
    QueryOrderDetailsResponse,
    QueryPendingOrderStatusResponse,
    QueryPositionHistoryResponse,
    QueryPositionModeResponse,
    QueryTwapEntrustedOrderResponse,
    QueryTwapHistoricalOrdersResponse,
    QueryTwapOrderDetailsResponse,
    SetLeverageResponse,
    SetPositionModeResponse,
    SwapQueryOrderHistoryResponse,
    SwitchMultiAssetsModeResponse,
    TestOrderResponse,
    UsersForceOrdersResponse,
)

if TYPE_CHECKING:
    from bingx_py.client import BingXHttpClient


class TradesAPI:
    """API for managing trades on BingX.

    This class provides methods to place, cancel, and query orders, manage positions,
    and interact with various trading features such as leverage, margin, and TWAP orders.
    """

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the TradesAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    def test_order(
        self,
        request: OrderRequest,
        recv_window: Optional[int] = None,
    ) -> TestOrderResponse:
        """Test placing an order.

        Args:
            request (OrderRequest): Order request model.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            TestOrderResponse: The response data.

        """
        params = request.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude_unset=True,
        )
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/order/test", params=params),
            TestOrderResponse,
        )

    def place_order_in_demo_trading(
        self,
        request: OrderRequest,
        recv_window: Optional[int] = None,
    ) -> PlaceOrderInDemoTradingResponse:
        """Place an order in demo trading.

        Args:
            request (OrderRequest): Order request model.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            PlaceOrderInDemoTradingResponse: The response data.

        """
        params: dict[str, Any] = request.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude_unset=True,
        )
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/order", params=params),
            PlaceOrderInDemoTradingResponse,
        )

    def place_order(
        self,
        request: OrderRequest,
        recv_window: Optional[int] = None,
    ) -> PlaceOrderResponse:
        """Place an order.

        Args:
            request (OrderRequest): Order request model.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            PlaceOrderResponse: The response data.

        """
        params = request.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude_unset=True,
        )
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/order", params=params),
            PlaceOrderResponse,
        )

    def place_multiple_orders(
        self,
        batch_orders: list["OrderRequest"],
        recv_window: Optional[int] = None,
    ) -> PlaceMultipleOrdersResponse:
        """Place multiple orders.

        Args:
            batch_orders (List[OrderRequest]): List of orders to place, supporting up to 5 orders.
            recv_window (Optional[int]): Request valid time window value in milliseconds. Defaults to None.

        Returns:
            PlaceMultipleOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "batchOrders": [
                order.model_dump(by_alias=True, exclude_none=True, exclude_unset=True)
                for order in batch_orders
            ],
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/batchOrders", params=params),
            PlaceMultipleOrdersResponse,
        )

    def close_all_positions(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> CloseAllPositionsResponse:
        """Close all positions.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Request valid time window value in milliseconds. Defaults to None.

        Returns:
            CloseAllPositionsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/closeAllPositions", params=params),
            CloseAllPositionsResponse,
        )

    def cancel_order(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> CancelOrderResponse:
        """Cancel an order.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_id (Optional[int]): Order ID. Defaults to None.
            client_order_id (Optional[str]): Customized order ID. Defaults to None.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            CancelOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if client_order_id is not None:
            params["clientOrderId"] = client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.delete("/openApi/swap/v2/trade/order", params=params),
            CancelOrderResponse,
        )

    def cancel_multiple_orders(
        self,
        symbol: str,
        order_id_list: Optional[list[int]] = None,
        client_order_id_list: Optional[list[str]] = None,
        recv_window: Optional[int] = None,
    ) -> CancelMultipleOrdersResponse:
        """Cancel multiple orders.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_id_list (Optional[List[int]]): List of order IDs. Defaults to None.
            client_order_id_list (Optional[List[str]]): List of customized order IDs. Defaults to None.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            CancelMultipleOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id_list is not None:
            params["orderIdList"] = order_id_list
        if client_order_id_list is not None:
            params["clientOrderIdList"] = client_order_id_list
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.delete("/openApi/swap/v2/trade/batchOrders", params=params),
            CancelMultipleOrdersResponse,
        )

    def cancel_all_open_orders(
        self,
        symbol: Optional[str] = None,
        order_type: Optional[OrderType] = None,
        recv_window: Optional[int] = None,
    ) -> CancelAllOpenOrdersResponse:
        """Cancel all open orders.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            order_type (Optional[OrderType]): Order type. Defaults to None.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            CancelAllOpenOrdersResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if order_type is not None:
            params["type"] = order_type.value
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.delete("/openApi/swap/v2/trade/allOpenOrders", params=params),
            CancelAllOpenOrdersResponse,
        )

    def get_current_all_open_orders(
        self,
        symbol: Optional[str] = None,
        order_type: Optional[OrderType] = None,
        recv_window: Optional[int] = None,
    ) -> CurrentAllOpenOrdersResponse:
        """Get current all open orders.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            order_type (Optional[OrderType]): Order type. Defaults to None.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            CurrentAllOpenOrdersResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if order_type is not None:
            params["type"] = order_type.value
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/openOrders", params=params),
            CurrentAllOpenOrdersResponse,
        )

    def query_pending_order_status(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryPendingOrderStatusResponse:
        """Query pending order status.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_id (Optional[int]): Order ID. Defaults to None.
            client_order_id (Optional[str]): Customized order ID. Defaults to None.
            recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

        Returns:
            QueryPendingOrderStatusResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if client_order_id is not None:
            params["clientOrderId"] = client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/openOrder", params=params),
            QueryPendingOrderStatusResponse,
        )

    def query_order_details(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryOrderDetailsResponse:
        """Query order details.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT. There must be a hyphen ("-") in the trading pair symbol.
            order_id (Optional[int]): Order ID. Defaults to None.
            client_order_id (Optional[str]): Customized order ID for users, with a limit of characters from 1 to 40. The system will convert this field to lowercase. Different orders cannot use the same clientOrderId. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryOrderDetailsResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if client_order_id is not None:
            params["clientOrderId"] = client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/order", params=params),
            QueryOrderDetailsResponse,
        )

    def query_margin_type(
        self,
        symbol: str,
        recv_window: Optional[int] = None,
    ) -> QueryMarginTypeResponse:
        """Query margin type for a trading pair.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT. There must be a hyphen ("-") in the trading pair symbol.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryMarginTypeResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/marginType", params=params),
            QueryMarginTypeResponse,
        )

    def change_margin_type(
        self,
        symbol: str,
        margin_type: MarginType,
        recv_window: Optional[int] = None,
    ) -> ChangeMarginTypeResponse:
        """Change margin type for a trading pair.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT. There must be a hyphen ("-") in the trading pair symbol.
            margin_type (MarginType): Margin mode (ISOLATED or CROSSED).
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            ChangeMarginTypeResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "marginType": margin_type.value,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/marginType", params=params),
            ChangeMarginTypeResponse,
        )

    def query_leverage_and_available_positions(
        self,
        symbol: str,
        recv_window: Optional[int] = None,
    ) -> QueryLeverageAndAvailablePositionsResponse:
        """Query leverage and available positions for a trading pair.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT. There must be a hyphen ("-") in the trading pair symbol.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryLeverageAndAvailablePositionsResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/leverage", params=params),
            QueryLeverageAndAvailablePositionsResponse,
        )

    def set_leverage(
        self,
        symbol: str,
        side: str,
        leverage: int,
        recv_window: Optional[int] = None,
    ) -> SetLeverageResponse:
        """Set leverage for a trading pair.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT. There must be a hyphen ("-") in the trading pair symbol.
            side (str): Leverage for long or short positions. In the Hedge mode, LONG for long positions, SHORT for short positions. In the One-way mode, only supports BOTH.
            leverage (int): Leverage value.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SetLeverageResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "leverage": leverage,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/leverage", params=params),
            SetLeverageResponse,
        )

    def users_force_orders(
        self,
        symbol: Optional[str] = None,
        currency: Optional[str] = None,
        auto_close_type: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> UsersForceOrdersResponse:
        """Query user's force orders.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            currency (Optional[str]): USDC or USDT. Defaults to None.
            auto_close_type (Optional[str]): "LIQUIDATION" or "ADL". Defaults to None.
            start_time (Optional[int]): Start time, unit: millisecond. Defaults to None.
            end_time (Optional[int]): End time, unit: millisecond. Defaults to None.
            limit (Optional[int]): The number of returned result sets. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            UsersForceOrdersResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if currency is not None:
            params["currency"] = currency
        if auto_close_type is not None:
            params["autoCloseType"] = auto_close_type
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/forceOrders", params=params),
            UsersForceOrdersResponse,
        )

    def query_order_history(
        self,
        symbol: Optional[str] = None,
        currency: Optional[str] = None,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
        recv_window: Optional[int] = None,
    ) -> SwapQueryOrderHistoryResponse:
        """Query order history.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            currency (Optional[str]): USDC or USDT. Defaults to None.
            order_id (Optional[int]): Order ID. Defaults to None.
            start_time (Optional[int]): Start time, unit: millisecond. Defaults to None.
            end_time (Optional[int]): End time, unit: millisecond. Defaults to None.
            limit (int): Number of result sets to return. Defaults to 500.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SwapQueryOrderHistoryResponse: The response data.

        """
        params: dict[str, Any] = {
            "limit": limit,
        }
        if symbol is not None:
            params["symbol"] = symbol
        if currency is not None:
            params["currency"] = currency
        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/allOrders", params=params),
            SwapQueryOrderHistoryResponse,
        )

    def modify_isolated_position_margin(
        self,
        symbol: str,
        amount: float,
        direction_type: int,
        position_side: Optional[str] = None,
        position_id: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> ModifyIsolatedPositionMarginResponse:
        """Modify isolated position margin.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            amount (float): Margin funds.
            direction_type (int): Adjustment direction (1: increase, 2: decrease).
            position_side (Optional[str]): Position direction (LONG or SHORT). Defaults to None.
            position_id (Optional[int]): Position ID. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            ModifyIsolatedPositionMarginResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "amount": amount,
            "direction_type": direction_type,
        }
        if position_side is not None:
            params["positionSide"] = position_side
        if position_id is not None:
            params["positionId"] = position_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/positionMargin", params=params),
            ModifyIsolatedPositionMarginResponse,
        )

    def get_trading_historical_orders(
        self,
        trading_unit: str,
        start_ts: int,
        end_ts: int,
        order_id: Optional[int] = None,
        currency: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryHistoricalTransactionOrdersResponse:
        """Query historical transaction orders.

        Args:
            order_id (Optional[int]): Order ID. Defaults to None.
            currency (Optional[str]): USDC or USDT. Defaults to None.
            trading_unit (str): Trading unit (COIN or CONT).
            start_ts (int): Starting timestamp in milliseconds.
            end_ts (int): End timestamp in milliseconds.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryHistoricalTransactionOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "tradingUnit": trading_unit,
            "startTs": start_ts,
            "endTs": end_ts,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if currency is not None:
            params["currency"] = currency
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/allFillOrders", params=params),
            QueryHistoricalTransactionOrdersResponse,
        )

    def set_position_mode(
        self,
        dual_side_position: bool,
        recv_window: Optional[int] = None,
    ) -> SetPositionModeResponse:
        """Set position mode.

        Args:
            dual_side_position (bool): "true" for dual position mode, "false" for single position mode.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SetPositionModeResponse: The response data.

        """
        params: dict[str, Any] = {
            "dualSidePosition": str(dual_side_position).lower(),
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/positionSide/dual", params=params),
            SetPositionModeResponse,
        )

    def query_position_mode(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryPositionModeResponse:
        """Query position mode.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryPositionModeResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/positionSide/dual", params=params),
            QueryPositionModeResponse,
        )

    def cancel_replace_order(
        self,
        request: CancelReplaceOrderRequest,
    ) -> CancelReplaceOrderResponse:
        """Cancel an existing order and place a new one.

        Args:
            request (CancelReplaceOrderRequest): The request object.

        Returns:
            CancelReplaceOrderResponse: The response data.

        """
        return self.client.save_convert(
            self.client.post(
                "/openApi/swap/v1/trade/cancelReplace",
                params=request.model_dump(
                    by_alias=True,
                    exclude_none=True,
                    exclude_unset=True,
                ),
            ),
            CancelReplaceOrderResponse,
        )

    def batch_cancel_replace_orders(
        self,
        batch_orders: list[CancelReplaceOrderRequest],
        recv_window: Optional[int] = None,
    ) -> BatchCancelReplaceOrdersResponse:
        """Cancel and replace multiple orders in batches.

        Args:
            batch_orders (List[Dict[str, Any]]): List of orders to cancel and replace.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            BatchCancelReplaceOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "batchOrders": [
                order.model_dump(by_alias=True, exclude_none=True, exclude_unset=True)
                for order in batch_orders
            ],
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post(
                "/openApi/swap/v1/trade/batchCancelReplace",
                params=params,
            ),
            BatchCancelReplaceOrdersResponse,
        )

    def cancel_all_after(
        self,
        state_type: str,
        time_out: int,
    ) -> CancelAllAfterResponse:
        """Cancel all orders after a specified time.

        Args:
            state_type (str): ACTIVATE or CLOSE.
            time_out (int): Timeout in seconds (10-120).

        Returns:
            CancelAllAfterResponse: The response data.

        """
        params: dict[str, Any] = {
            "type": state_type,
            "timeOut": time_out,
        }

        return self.client.save_convert(
            self.client.post("/openApi/swap/v2/trade/cancelAllAfter", params=params),
            CancelAllAfterResponse,
        )

    def close_position_by_id(
        self,
        position_id: str,
        recv_window: Optional[int] = None,
    ) -> ClosePositionResponse:
        """Close a position by its ID.

        Args:
            position_id (str): The position ID to close.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            ClosePositionResponse: The response data.

        """
        params: dict[str, Any] = {
            "positionId": position_id,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/trade/closePosition", params=params),
            ClosePositionResponse,
        )

    def query_all_orders(
        self,
        symbol: Optional[str] = None,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: int = 500,
        recv_window: Optional[int] = None,
    ) -> QueryAllOrdersResponse:
        """Query all orders.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            order_id (Optional[int]): Order ID. Defaults to None.
            start_time (Optional[int]): Start time in milliseconds. Defaults to None.
            end_time (Optional[int]): End time in milliseconds. Defaults to None.
            limit (int): Number of orders to return. Defaults to 500.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            QueryAllOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "limit": limit,
        }
        if symbol is not None:
            params["symbol"] = symbol
        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/trade/fullOrder", params=params),
            QueryAllOrdersResponse,
        )

    def position_and_maintenance_margin_ratio(
        self,
        symbol: str,
        recv_window: Optional[int] = None,
    ) -> PositionAndMaintenanceMarginRatioResponse:
        """Query position and maintenance margin ratio.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            PositionAndMaintenanceMarginRatioResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/maintMarginRatio", params=params),
            PositionAndMaintenanceMarginRatioResponse,
        )

    def query_historical_transaction_details(
        self,
        symbol: str,
        start_ts: int,
        end_ts: int,
        currency: Optional[str] = None,
        order_id: Optional[int] = None,
        last_fill_id: Optional[int] = None,
        page_index: Optional[int] = None,
        page_size: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QueryHistoricalTransactionDetailsResponse:
        """Query historical transaction details.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            start_ts (int): Starting timestamp in milliseconds.
            end_ts (int): End timestamp in milliseconds.
            currency (Optional[str]): USDC or USDT. Defaults to None.
            order_id (Optional[int]): Order ID. Defaults to None.
            last_fill_id (Optional[int]): The last tradeId of the last query. Defaults to None.
            page_index (Optional[int]): Page number. Defaults to None.
            page_size (Optional[int]): Page size. Defaults to None.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            QueryHistoricalTransactionDetailsResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "startTs": start_ts,
            "endTs": end_ts,
        }
        if currency is not None:
            params["currency"] = currency
        if order_id is not None:
            params["orderId"] = order_id
        if last_fill_id is not None:
            params["lastFillId"] = last_fill_id
        if page_index is not None:
            params["pageIndex"] = page_index
        if page_size is not None:
            params["pageSize"] = page_size
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/trade/fillHistory", params=params),
            QueryHistoricalTransactionDetailsResponse,
        )

    def query_position_history(
        self,
        start_ts: int,
        end_ts: int,
        symbol: Optional[str] = None,
        currency: Optional[str] = None,
        position_id: Optional[int] = None,
        page_index: Optional[int] = None,
        page_size: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QueryPositionHistoryResponse:
        """Query position history.

        Args:
            start_ts (int): Start timestamp in milliseconds.
            end_ts (int): End timestamp in milliseconds.
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            currency (Optional[str]): USDC or USDT. Defaults to None.
            position_id (Optional[int]): Position ID. Defaults to None.
            page_index (Optional[int]): Page number. Defaults to None.
            page_size (Optional[int]): Page size. Defaults to None.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            QueryPositionHistoryResponse: The response data.

        """
        params: dict[str, Any] = {
            "startTs": start_ts,
            "endTs": end_ts,
        }
        if symbol is not None:
            params["symbol"] = symbol
        if currency is not None:
            params["currency"] = currency
        if position_id is not None:
            params["positionId"] = position_id
        if page_index is not None:
            params["pageIndex"] = page_index
        if page_size is not None:
            params["pageSize"] = page_size
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/trade/positionHistory", params=params),
            QueryPositionHistoryResponse,
        )

    def isolated_margin_change_history(
        self,
        symbol: str,
        position_id: str,
        start_time: int,
        end_time: int,
        page_index: int,
        page_size: int,
        recv_window: Optional[int] = None,
    ) -> IsolatedMarginChangeHistoryResponse:
        """Query isolated margin change history.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            position_id (str): Position ID.
            start_time (int): Start timestamp in milliseconds.
            end_time (int): End timestamp in milliseconds.
            page_index (int): Page number, must be greater than 0.
            page_size (int): Page size, must be greater than 0.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            IsolatedMarginChangeHistoryResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "positionId": position_id,
            "startTime": start_time,
            "endTime": end_time,
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/positionMargin/history", params=params),
            IsolatedMarginChangeHistoryResponse,
        )

    def apply_vst(
        self,
        recv_window: Optional[int] = None,
    ) -> ApplyVstResponse:
        """Apply VST.

        Args:
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            ApplyVstResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/trade/getVst", params=params),
            ApplyVstResponse,
        )

    def place_twap_order(
        self,
        symbol: str,
        side: str,
        position_side: str,
        price_type: str,
        price_variance: str,
        trigger_price: str,
        interval: int,
        amount_per_order: str,
        total_amount: str,
        recv_window: Optional[int] = None,
    ) -> PlaceTwapOrderResponse:
        """Place a TWAP order.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            side (str): Buying and selling direction (SELL, BUY).
            position_side (str): LONG or SHORT.
            price_type (str): Price limit type (constant or percentage).
            price_variance (str): Price difference or slippage ratio.
            trigger_price (str): Trigger price.
            interval (int): Time interval for order placing (5-120s).
            amount_per_order (str): Quantity of a single order.
            total_amount (str): Total trading volume.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            PlaceTwapOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "positionSide": position_side,
            "priceType": price_type,
            "priceVariance": price_variance,
            "triggerPrice": trigger_price,
            "interval": interval,
            "amountPerOrder": amount_per_order,
            "totalAmount": total_amount,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/twap/order", params=params),
            PlaceTwapOrderResponse,
        )

    def query_twap_entrusted_order(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryTwapEntrustedOrderResponse:
        """Query TWAP entrusted orders.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            QueryTwapEntrustedOrderResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/twap/openOrders", params=params),
            QueryTwapEntrustedOrderResponse,
        )

    def query_twap_historical_orders(
        self,
        page_index: int,
        page_size: int,
        start_time: int,
        end_time: int,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryTwapHistoricalOrdersResponse:
        """Query TWAP historical orders.

        Args:
            page_index (int): Page number, must be greater than 0.
            page_size (int): Page size, must be greater than 0.
            start_time (int): Start timestamp in milliseconds.
            end_time (int): End timestamp in milliseconds.
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            QueryTwapHistoricalOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "startTime": start_time,
            "endTime": end_time,
        }
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/twap/historyOrders", params=params),
            QueryTwapHistoricalOrdersResponse,
        )

    def query_twap_order_details(
        self,
        main_order_id: str,
        recv_window: Optional[int] = None,
    ) -> QueryTwapOrderDetailsResponse:
        """Query TWAP order details.

        Args:
            main_order_id (str): TWAP order number.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            QueryTwapOrderDetailsResponse: The response data.

        """
        params: dict[str, Any] = {
            "mainOrderId": main_order_id,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/twap/orderDetail", params=params),
            QueryTwapOrderDetailsResponse,
        )

    def cancel_twap_order(
        self,
        main_order_id: str,
        recv_window: Optional[int] = None,
    ) -> CancelTwapOrderResponse:
        """Cancel a TWAP order.

        Args:
            main_order_id (str): TWAP order number.
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            CancelTwapOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "mainOrderId": main_order_id,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/twap/cancelOrder", params=params),
            CancelTwapOrderResponse,
        )

    def switch_multi_assets_mode(
        self,
        asset_mode: str,
        recv_window: Optional[int] = None,
    ) -> SwitchMultiAssetsModeResponse:
        """Switch multi-assets mode.

        Args:
            asset_mode (str): Multi-assets mode (singleAssetMode or multiAssetsMode).
            recv_window (Optional[int]): Request valid time window, Unit: milliseconds. Defaults to None.

        Returns:
            SwitchMultiAssetsModeResponse: The response data.

        """
        params: dict[str, Any] = {
            "assetMode": asset_mode,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/trade/assetMode", params=params),
            SwitchMultiAssetsModeResponse,
        )

    def query_multi_assets_mode(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryMultiAssetsModeResponse:
        """Query the current multi-assets mode.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryMultiAssetsModeResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/trade/assetMode", params=params),
            QueryMultiAssetsModeResponse,
        )

    def query_multi_assets_rules(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryMultiAssetsRulesResponse:
        """Query the rules for multi-assets mode.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryMultiAssetsRulesResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/trade/multiAssetsRules", params=params),
            QueryMultiAssetsRulesResponse,
        )

    def query_multi_assets_margin(
        self,
        recv_window: Optional[int] = None,
    ) -> QueryMultiAssetsMarginResponse:
        """Query the margin details for multi-assets mode.

        Args:
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryMultiAssetsMarginResponse: The response data.

        """
        params: dict[str, Any] = {}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/user/marginAssets", params=params),
            QueryMultiAssetsMarginResponse,
        )

    def one_click_reverse_position(
        self,
        reverse_type: str,
        symbol: str,
        trigger_price: Optional[str] = None,
        working_type: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> OneClickReversePositionResponse:
        """Perform a one-click reverse position.

        Args:
            reverse_type (str): Reverse type, Reverse: immediate reverse, TriggerReverse: planned reverse.
            symbol (str): Trading pair, e.g.: BTC-USDT.
            trigger_price (Optional[str]): Trigger price, required for planned reverse. Defaults to None.
            working_type (Optional[str]): TriggerPrice price type: MARK_PRICE, CONTRACT_PRICE, INDEX_PRICE, CONTRACT_PRICE. Required for planned reverse. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            OneClickReversePositionResponse: The response data.

        """
        params: dict[str, Any] = {
            "type": reverse_type,
            "symbol": symbol,
        }
        if trigger_price is not None:
            params["triggerPrice"] = trigger_price
        if working_type is not None:
            params["workingType"] = working_type
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/trade/reverse", params=params),
            OneClickReversePositionResponse,
        )

    def hedge_mode_auto_add_margin(
        self,
        symbol: str,
        position_id: int,
        function_switch: str,
        amount: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> HedgeModeAutoAddMarginResponse:
        """Enable or disable automatic margin addition for a hedge mode position.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT, please use uppercase letters.
            position_id (int): Position ID.
            function_switch (str): Whether to enable the automatic margin addition feature, true: enable, false: disable.
            amount (Optional[str]): Amount of margin to be added, in USDT. Must be specified when enabling the feature. Defaults to None.
            recv_window (Optional[int]): Request validity window, in milliseconds. Defaults to None.

        Returns:
            HedgeModeAutoAddMarginResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "positionId": position_id,
            "functionSwitch": function_switch,
        }
        if amount is not None:
            params["amount"] = amount
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/swap/v1/trade/autoAddMargin", params=params),
            HedgeModeAutoAddMarginResponse,
        )
