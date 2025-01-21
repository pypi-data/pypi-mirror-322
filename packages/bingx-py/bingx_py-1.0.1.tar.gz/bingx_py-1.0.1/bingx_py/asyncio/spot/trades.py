from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.general import OrderSide, OrderStatus, TimeInForce
from bingx_py.models.spot.trades import (
    CancelAllAfterType,
    CancelOcoOrderResponse,
    CancelReplaceMode,
    CancelRestrictions,
    CreateOcoOrderResponse,
    CurrentOpenOrdersResponse,
    PlaceOrderRequest,
    QueryAllOpenOcoOrdersResponse,
    QueryOcoHistoricalOrderListResponse,
    QueryOcoOrderListResponse,
    QueryOrderHistoryResponse,
    QueryTradingCommissionRateResponse,
    QueryTransactionDetailsResponse,
    SpotCancelAllAfterResponse,
    SpotCancelAllOpenOrdersResponse,
    SpotCancelMultipleOrdersResponse,
    SpotCancelOrderResponse,
    SpotCancelReplaceOrderResponse,
    SpotOrderType,
    SpotPlaceMultipleOrdersResponse,
    SpotPlaceOrderResponse,
    SpotQueryOrderDetailsResponse,
)

if TYPE_CHECKING:
    from bingx_py.asyncio import BingXHttpClient


class TradesAPI:
    """API for managing trades on BingX."""

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the TradesAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    def place_order(
        self,
        symbol: str,
        side: OrderSide,
        order_type: SpotOrderType,
        stop_price: Optional[str] = None,
        quantity: Optional[float] = None,
        quote_order_qty: Optional[float] = None,
        price: Optional[float] = None,
        new_client_order_id: Optional[str] = None,
        time_in_force: Optional[TimeInForce] = None,
        recv_window: Optional[float] = None,
    ) -> SpotPlaceOrderResponse:
        """Place an order.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            side (OrderSide): BUY/SELL.
            order_type (SpotOrderType): MARKET/LIMIT/TAKE_STOP_LIMIT/TAKE_STOP_MARKET/TRIGGER_LIMIT/TRIGGER_MARKET.
            stop_price (Optional[str]): Order trigger price, used for TAKE_STOP_LIMIT, TAKE_STOP_MARKET, TRIGGER_LIMIT, TRIGGER_MARKET type orders. Defaults to None.
            quantity (Optional[float]): Original quantity, e.g., 0.1BTC. Defaults to None.
            quote_order_qty (Optional[float]): Quote order quantity, e.g., 100USDT. If quantity and quote_order_qty are input at the same time, quantity will be used first. Defaults to None.
            price (Optional[float]): Price, e.g., 10000USDT. Defaults to None.
            new_client_order_id (Optional[str]): Customized order ID for users, with a limit of characters from 1 to 40. Defaults to None.
            time_in_force (Optional[TimeInForce]): Time in force, currently supports PostOnly, GTC, IOC, FOK. Default is GTC if not specified. Defaults to None.
            recv_window (Optional[float]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SpotPlaceOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side.value,
            "type": order_type.value,
        }
        if stop_price is not None:
            params["stopPrice"] = stop_price
        if quantity is not None:
            params["quantity"] = quantity
        if quote_order_qty is not None:
            params["quoteOrderQty"] = quote_order_qty
        if price is not None:
            params["price"] = price
        if new_client_order_id is not None:
            params["newClientOrderId"] = new_client_order_id
        if time_in_force is not None:
            params["timeInForce"] = time_in_force.value
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/trade/order", params=params),
            SpotPlaceOrderResponse,
        )

    def place_multiple_orders(
        self,
        data: list[PlaceOrderRequest],
        sync: Optional[bool] = None,
    ) -> SpotPlaceMultipleOrdersResponse:
        """Place multiple orders.

        Args:
            data (List[PlaceOrderRequest]): The request array for placing orders, limited to 5 orders.
            sync (Optional[bool]): sync=false (default false if not filled in): parallel ordering (but all orders need to have the same symbol/side/type), sync = true (multiple orders are ordered serially, all orders do not require the same symbol/side/type). Defaults to None.

        Returns:
            SpotPlaceMultipleOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "data": [
                order.model_dump(by_alias=True, exclude_none=True, exclude_unset=True)
                for order in data
            ],
        }
        if sync is not None:
            params["sync"] = sync

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/trade/batchOrders", params=params),
            SpotPlaceMultipleOrdersResponse,
        )

    def query_order_details(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        recv_window: Optional[float] = None,
    ) -> SpotQueryOrderDetailsResponse:
        """Query order details.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_id (Optional[int]): Order ID. Defaults to None.
            client_order_id (Optional[str]): Customized order ID for users, with a limit of characters from 1 to 40. Defaults to None.
            recv_window (Optional[float]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SpotQueryOrderDetailsResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if client_order_id is not None:
            params["clientOrderID"] = client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/trade/query", params=params),
            SpotQueryOrderDetailsResponse,
        )

    def current_open_orders(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[float] = None,
    ) -> CurrentOpenOrdersResponse:
        """Query current open orders.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Query all pending orders when left blank. Defaults to None.
            recv_window (Optional[float]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            CurrentOpenOrdersResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/trade/openOrders", params=params),
            CurrentOpenOrdersResponse,
        )

    def query_order_history(
        self,
        symbol: Optional[str] = None,
        order_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page_index: Optional[int] = None,
        page_size: Optional[int] = None,
        status: Optional[OrderStatus] = None,
        order_type: Optional[SpotOrderType] = None,
        recv_window: Optional[int] = None,
    ) -> QueryOrderHistoryResponse:
        """Query order history.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            order_id (Optional[int]): If orderId is set, orders >= orderId. Otherwise, the most recent orders will be returned. Defaults to None.
            start_time (Optional[int]): Start timestamp, Unit: ms. Defaults to None.
            end_time (Optional[int]): End timestamp, Unit: ms. Defaults to None.
            page_index (Optional[int]): Page number, must >0. If not specified, it defaults to 1. Restriction: pageIndex * pageSize <= 10,000. Defaults to None.
            page_size (Optional[int]): Page size, must >0. Max 100. If not specified, it defaults to 100. Restriction: pageIndex * pageSize <= 10,000. Defaults to None.
            status (Optional[OrderStatus]): Order status: FILLED (fully filled) CANCELED: (canceled) FAILED: (failed). Defaults to None.
            order_type (Optional[SpotOrderType]): Order type: MARKET/LIMIT/TAKE_STOP_LIMIT/TAKE_STOP_MARKET/TRIGGER_LIMIT/TRIGGER_MARKET. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            QueryOrderHistoryResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if page_index is not None:
            params["pageIndex"] = page_index
        if page_size is not None:
            params["pageSize"] = page_size
        if status is not None:
            params["status"] = status.value
        if order_type is not None:
            params["type"] = order_type.value
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/trade/historyOrders", params=params),
            QueryOrderHistoryResponse,
        )

    def query_trading_commission_rate(
        self,
        symbol: str,
        recv_window: Optional[float] = None,
    ) -> QueryTradingCommissionRateResponse:
        """Query trading commission rate.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            recv_window (Optional[float]): Request valid time window in milliseconds. Defaults to None.

        Returns:
            QueryTradingCommissionRateResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/user/commissionRate", params=params),
            QueryTradingCommissionRateResponse,
        )

    def cancel_all_after(
        self,
        cancel_type: CancelAllAfterType,
        time_out: int,
    ) -> SpotCancelAllAfterResponse:
        """Cancel all orders after a specified time.

        Args:
            cancel_type (CancelAllAfterType): Request type: ACTIVATE-Activate, CLOSE-Close.
            time_out (int): Activate countdown time (seconds), range: 10s-120s.

        Returns:
            SpotCancelAllAfterResponse: The response data.

        """
        params: dict[str, Any] = {
            "type": cancel_type.value,
            "timeOut": time_out,
        }

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/trade/cancelAllAfter", params=params),
            SpotCancelAllAfterResponse,
        )

    def cancel_order(
        self,
        symbol: str,
        order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        cancel_restrictions: Optional[CancelRestrictions] = None,
        recv_window: Optional[float] = None,
    ) -> SpotCancelOrderResponse:
        """Cancel an order.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_id (Optional[int]): Order ID. Defaults to None.
            client_order_id (Optional[str]): Customized order ID for users, with a limit of characters from 1 to 40. Defaults to None.
            cancel_restrictions (Optional[CancelRestrictions]): Cancel orders with specified status: NEW, PENDING, PARTIALLY_FILLED. Defaults to None.
            recv_window (Optional[float]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SpotCancelOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if order_id is not None:
            params["orderId"] = order_id
        if client_order_id is not None:
            params["clientOrderID"] = client_order_id
        if cancel_restrictions is not None:
            params["cancelRestrictions"] = cancel_restrictions.value
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/trade/cancel", params=params),
            SpotCancelOrderResponse,
        )

    def cancel_multiple_orders(
        self,
        symbol: str,
        order_ids: str,
        process: Optional[int] = None,
        client_order_ids: Optional[str] = None,
        recv_window: Optional[float] = None,
    ) -> SpotCancelMultipleOrdersResponse:
        """Cancel multiple orders.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_ids (str): Order IDs, e.g., orderIds=id1,id2,id3.
            process (Optional[int]): 0 or 1, default 0. If process=1, will handle valid orderIds partially, and return invalid orderIds in fails list. If process=0, if one of orderIds invalid, will all fail. Defaults to None.
            client_order_ids (Optional[str]): Custom order IDs, e.g., clientOrderIDs=id1,id2,id3. Defaults to None.
            recv_window (Optional[float]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SpotCancelMultipleOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "orderIds": order_ids,
        }
        if process is not None:
            params["process"] = process
        if client_order_ids is not None:
            params["clientOrderIDs"] = client_order_ids
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/trade/cancelOrders", params=params),
            SpotCancelMultipleOrdersResponse,
        )

    def cancel_all_open_orders(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[float] = None,
    ) -> SpotCancelAllOpenOrdersResponse:
        """Cancel all open orders on a symbol.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. If not filled out, cancel all orders. Defaults to None.
            recv_window (Optional[float]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SpotCancelAllOpenOrdersResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/trade/cancelOpenOrders", params=params),
            SpotCancelAllOpenOrdersResponse,
        )

    def cancel_replace_order(
        self,
        symbol: str,
        cancel_replace_mode: CancelReplaceMode,
        side: OrderSide,
        order_type: SpotOrderType,
        stop_price: str,
        cancel_order_id: Optional[int] = None,
        cancel_client_order_id: Optional[str] = None,
        cancel_restrictions: Optional[CancelRestrictions] = None,
        quantity: Optional[float] = None,
        quote_order_qty: Optional[float] = None,
        price: Optional[float] = None,
        new_client_order_id: Optional[str] = None,
        recv_window: Optional[float] = None,
    ) -> SpotCancelReplaceOrderResponse:
        """Cancel an existing order and send a new order.

        Args:
            symbol (str): The trading pair, e.g., BTC-USDT.
            cancel_replace_mode (CancelReplaceMode): STOP_ON_FAILURE or ALLOW_FAILURE.
            side (OrderSide): BUY or SELL.
            order_type (SpotOrderType): MARKET/LIMIT/TAKE_STOP_LIMIT/TAKE_STOP_MARKET/TRIGGER_LIMIT/TRIGGER_MARKET.
            stop_price (str): Trigger price used for TAKE_STOP_LIMIT, TAKE_STOP_MARKET, TRIGGER_LIMIT, TRIGGER_MARKET order types.
            cancel_order_id (Optional[int]): The ID of the order to be canceled. Defaults to None.
            cancel_client_order_id (Optional[str]): The user-defined ID of the order to be canceled. Defaults to None.
            cancel_restrictions (Optional[CancelRestrictions]): Cancel orders with specified status: NEW, PENDING, PARTIALLY_FILLED. Defaults to None.
            quantity (Optional[float]): Order quantity, e.g., 0.1 BTC. Defaults to None.
            quote_order_qty (Optional[float]): Order amount, e.g., 100 USDT. Defaults to None.
            price (Optional[float]): Order price, e.g., 10000 USDT. Defaults to None.
            new_client_order_id (Optional[str]): Custom order ID consisting of letters, numbers, and _. Defaults to None.
            recv_window (Optional[float]): Request valid time window in milliseconds. Defaults to None.

        Returns:
            SpotCancelReplaceOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "CancelReplaceMode": cancel_replace_mode.value,
            "side": side.value,
            "type": order_type.value,
            "stopPrice": stop_price,
        }
        if cancel_order_id is not None:
            params["cancelOrderId"] = cancel_order_id
        if cancel_client_order_id is not None:
            params["cancelClientOrderID"] = cancel_client_order_id
        if cancel_restrictions is not None:
            params["cancelRestrictions"] = cancel_restrictions.value
        if quantity is not None:
            params["quantity"] = quantity
        if quote_order_qty is not None:
            params["quoteOrderQty"] = quote_order_qty
        if price is not None:
            params["price"] = price
        if new_client_order_id is not None:
            params["newClientOrderId"] = new_client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post(
                "/openApi/spot/v1/trade/order/cancelReplace",
                params=params,
            ),
            SpotCancelReplaceOrderResponse,
        )

    def query_transaction_details(
        self,
        symbol: str,
        order_id: int,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        from_id: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[float] = None,
    ) -> QueryTransactionDetailsResponse:
        """Query transaction details.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            order_id (int): Order ID.
            start_time (Optional[int]): Start timestamp, unit: ms. Defaults to None.
            end_time (Optional[int]): End timestamp, unit: ms. Defaults to None.
            from_id (Optional[int]): Starting trade ID. By default, the latest trade will be retrieved. Defaults to None.
            limit (Optional[int]): Default 500, maximum 1000. Defaults to None.
            recv_window (Optional[float]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            QueryTransactionDetailsResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "orderId": order_id,
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if from_id is not None:
            params["fromId"] = from_id
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/trade/myTrades", params=params),
            QueryTransactionDetailsResponse,
        )

    def create_oco_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        limit_price: float,
        order_price: float,
        trigger_price: float,
        list_client_order_id: Optional[str] = None,
        above_client_order_id: Optional[str] = None,
        below_client_order_id: Optional[str] = None,
        recv_window: Optional[float] = None,
    ) -> CreateOcoOrderResponse:
        """Create an OCO order.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            side (OrderSide): BUY or SELL.
            quantity (float): Order quantity, e.g., 0.1 BTC.
            limit_price (float): Limit order price, e.g., 10000 USDT.
            order_price (float): The limit order price set after a stop-limit order is triggered, e.g., 10000 USDT.
            trigger_price (float): The trigger price of the stop-limit order, e.g., 10000 USDT.
            list_client_order_id (Optional[str]): Custom unique ID for the entire Order List. Defaults to None.
            above_client_order_id (Optional[str]): Custom unique ID for the limit order. Defaults to None.
            below_client_order_id (Optional[str]): Custom unique ID for the stop-limit order. Defaults to None.
            recv_window (Optional[float]): Request validity time window, in milliseconds. Defaults to None.

        Returns:
            CreateOcoOrderResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side.value,
            "quantity": quantity,
            "limitPrice": limit_price,
            "orderPrice": order_price,
            "triggerPrice": trigger_price,
        }
        if list_client_order_id is not None:
            params["listClientOrderId"] = list_client_order_id
        if above_client_order_id is not None:
            params["aboveClientOrderId"] = above_client_order_id
        if below_client_order_id is not None:
            params["belowClientOrderId"] = below_client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/oco/order", params=params),
            CreateOcoOrderResponse,
        )

    def cancel_oco_order(
        self,
        order_id: Optional[str] = None,
        client_order_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> CancelOcoOrderResponse:
        """Cancel an OCO order list.

        Args:
            order_id (Optional[str]): The order ID of the limit order or the stop-limit order. Defaults to None.
            client_order_id (Optional[str]): The User-defined order ID of the limit order or the stop-limit order. Defaults to None.
            recv_window (Optional[int]): Request validity window, in milliseconds. Defaults to None.

        Returns:
            CancelOcoOrderResponse: The response data.

        """
        params: dict[str, Any] = {}
        if order_id is not None:
            params["orderId"] = order_id
        if client_order_id is not None:
            params["clientOrderId"] = client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.post("/openApi/spot/v1/oco/cancel", params=params),
            CancelOcoOrderResponse,
        )

    def query_oco_order_list(
        self,
        order_list_id: Optional[str] = None,
        client_order_id: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> QueryOcoOrderListResponse:
        """Query an OCO order list.

        Args:
            order_list_id (Optional[str]): OCO order group ID. Defaults to None.
            client_order_id (Optional[str]): User-defined OCO order group ID. Defaults to None.
            recv_window (Optional[int]): Request valid time window, in milliseconds. Defaults to None.

        Returns:
            QueryOcoOrderListResponse: The response data.

        """
        params: dict[str, Any] = {}
        if order_list_id is not None:
            params["orderListId"] = order_list_id
        if client_order_id is not None:
            params["clientOrderId"] = client_order_id
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/oco/orderList", params=params),
            QueryOcoOrderListResponse,
        )

    def query_all_open_oco_orders(
        self,
        page_index: int,
        page_size: int,
        recv_window: Optional[int] = None,
    ) -> QueryAllOpenOcoOrdersResponse:
        """Query all open OCO orders.

        Args:
            page_index (int): Page number.
            page_size (int): Number of items per page.
            recv_window (Optional[int]): Request validity window, in milliseconds. Defaults to None.

        Returns:
            QueryAllOpenOcoOrdersResponse: The response data.

        """
        params: dict[str, Any] = {
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/oco/openOrderList", params=params),
            QueryAllOpenOcoOrdersResponse,
        )

    def query_oco_historical_order_list(
        self,
        page_index: int,
        page_size: int,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> QueryOcoHistoricalOrderListResponse:
        """Query OCO historical order list.

        Args:
            page_index (int): Page number.
            page_size (int): Number of items per page.
            start_time (Optional[int]): Start time, timestamp, in milliseconds. Defaults to None.
            end_time (Optional[int]): End time, timestamp, in milliseconds. Defaults to None.
            recv_window (Optional[int]): Request validity window, in milliseconds. Defaults to None.

        Returns:
            QueryOcoHistoricalOrderListResponse: The response data.

        """
        params: dict[str, Any] = {
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/spot/v1/oco/historyOrderList", params=params),
            QueryOcoHistoricalOrderListResponse,
        )
