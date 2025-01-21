from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from bingx_py.models.general import OrderSide, OrderStatus, TimeInForce


class SpotOrderType(str, Enum):
    """Enum for spot order types.

    Args:
        MARKET (str): Market order.
        LIMIT (str): Limit order.
        TAKE_STOP_LIMIT (str): Take profit/stop loss limit order.
        TAKE_STOP_MARKET (str): Take profit/stop loss market order.
        TRIGGER_LIMIT (str): Trigger limit order.
        TRIGGER_MARKET (str): Trigger market order.

    """

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    TAKE_STOP_LIMIT = "TAKE_STOP_LIMIT"
    TAKE_STOP_MARKET = "TAKE_STOP_MARKET"
    TRIGGER_LIMIT = "TRIGGER_LIMIT"
    TRIGGER_MARKET = "TRIGGER_MARKET"


class PlaceOrderRequest(BaseModel):
    """Model for the request of PlaceOrder.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        side (OrderSide): BUY/SELL.
        type (SpotOrderType): MARKET/LIMIT/TAKE_STOP_LIMIT/TAKE_STOP_MARKET/TRIGGER_LIMIT/TRIGGER_MARKET.
        stop_price (Optional[str]): Order trigger price, used for TAKE_STOP_LIMIT, TAKE_STOP_MARKET, TRIGGER_LIMIT, TRIGGER_MARKET type orders. Defaults to None.
        quantity (Optional[float]): Original quantity, e.g., 0.1BTC. Defaults to None.
        quote_order_qty (Optional[float]): Quote order quantity, e.g., 100USDT. If quantity and quote_order_qty are input at the same time, quantity will be used first. Defaults to None.
        price (Optional[float]): Price, e.g., 10000USDT. Defaults to None.
        new_client_order_id (Optional[str]): Customized order ID for users, with a limit of characters from 1 to 40. Defaults to None.
        time_in_force (Optional[TimeInForce]): Time in force, currently supports PostOnly, GTC, IOC, FOK. Default is GTC if not specified. Defaults to None.

    """

    symbol: str
    side: OrderSide
    type: SpotOrderType
    stop_price: Optional[str] = Field(None, serialization_alias="stopPrice")
    quantity: Optional[float] = None
    quote_order_qty: Optional[float] = Field(None, serialization_alias="quoteOrderQty")
    price: Optional[float] = None
    new_client_order_id: Optional[str] = Field(
        None,
        serialization_alias="newClientOrderId",
    )
    time_in_force: Optional[TimeInForce] = Field(
        None,
        serialization_alias="timeInForce",
    )


class SpotPlaceOrderResponse(BaseModel):
    """Model for the response of PlaceOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (PlaceOrderData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "PlaceOrderData"


class PlaceOrderData(BaseModel):
    """Model for the response data of PlaceOrder.

    Args:
        symbol (str): Trading pair.
        order_id (int): Order ID.
        transact_time (int): Transaction timestamp.
        price (str): Price.
        orig_qty (str): Original quantity.
        executed_qty (str): Executed quantity.
        cummulative_quote_qty (str): Cumulative quote asset transacted quantity.
        status (OrderStatus): Order status.
        type (SpotOrderType): Order type.
        side (OrderSide): BUY/SELL.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    transact_time: int = Field(..., alias="transactTime")
    price: str
    orig_qty: str = Field(..., alias="origQty")
    executed_qty: str = Field(..., alias="executedQty")
    cummulative_quote_qty: str = Field(..., alias="cummulativeQuoteQty")
    status: OrderStatus
    type: SpotOrderType
    side: OrderSide


class SpotPlaceMultipleOrdersResponse(BaseModel):
    """Model for the response of PlaceMultipleOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (PlaceMultipleOrdersData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "PlaceMultipleOrdersData"


class PlaceMultipleOrdersData(BaseModel):
    """Model for the response data of PlaceMultipleOrders.

    Args:
        orders (List[PlaceOrderData]): Response array for a single order.

    """

    orders: list[PlaceOrderData]


class SpotQueryOrderDetailsResponse(BaseModel):
    """Model for the response of QueryOrderDetails.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (QueryOrderDetailsData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "QueryOrderDetailsData"


class QueryOrderDetailsData(BaseModel):
    """Model for the response data of QueryOrderDetails.

    Args:
        symbol (str): Trading pair.
        order_id (int): Order ID.
        price (str): Price.
        stop_price (str): Trigger price.
        orig_qty (str): Original quantity.
        executed_qty (str): Executed quantity.
        cummulative_quote_qty (str): Cumulative quote asset transacted quantity.
        status (OrderStatus): Order status.
        type (SpotOrderType): Order type.
        side (OrderSide): BUY/SELL.
        time (int): Order timestamp.
        update_time (int): Update timestamp.
        orig_quote_order_qty (str): Original quote order quantity.
        fee (str): Fee.
        fee_asset (str): Fee asset.
        client_order_id (Optional[str]): Customized order ID for users.
        avg_price (str): Average fill price.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    price: str
    stop_price: str = Field(..., alias="StopPrice")
    orig_qty: str = Field(..., alias="origQty")
    executed_qty: str = Field(..., alias="executedQty")
    cummulative_quote_qty: str = Field(..., alias="cummulativeQuoteQty")
    status: OrderStatus
    type: SpotOrderType
    side: OrderSide
    time: int
    update_time: int = Field(..., alias="updateTime")
    orig_quote_order_qty: str = Field(..., alias="origQuoteOrderQty")
    fee: str
    fee_asset: str = Field(..., alias="feeAsset")
    client_order_id: Optional[str] = Field(None, alias="clientOrderID")
    avg_price: str = Field(..., alias="avgPrice")


class CurrentOpenOrdersResponse(BaseModel):
    """Model for the response of CurrentOpenOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CurrentOpenOrdersData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CurrentOpenOrdersData"


class CurrentOpenOrdersData(BaseModel):
    """Model for the response data of CurrentOpenOrders.

    Args:
        orders (List[QueryOrderDetailsData]): Order list, max length is 2000.

    """

    orders: list[QueryOrderDetailsData]


class QueryOrderHistoryResponse(BaseModel):
    """Model for the response of QueryOrderHistory.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (QueryOrderHistoryData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "QueryOrderHistoryData"


class QueryOrderHistoryData(BaseModel):
    """Model for the response data of QueryOrderHistory.

    Args:
        orders (List[QueryOrderDetailsData]): Order list, max length is 2000.

    """

    orders: list[QueryOrderDetailsData]


class CancelAllAfterType(str, Enum):
    """Enum for cancel all after type.

    Values:
        ACTIVATE: Activate the cancel all after feature.
        CLOSE: Close the cancel all after feature.
    """

    ACTIVATE = "ACTIVATE"
    CLOSE = "CLOSE"


class CancelRestrictions(str, Enum):
    """Enum for cancel restrictions.

    Values:
        NEW: Restrict cancellation to new orders.
        PENDING: Restrict cancellation to pending orders.
        PARTIALLY_FILLED: Restrict cancellation to partially filled orders.
    """

    NEW = "NEW"
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"


class QueryTradingCommissionRateResponse(BaseModel):
    """Model for the response of QueryTradingCommissionRate.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (QueryTradingCommissionRateData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "QueryTradingCommissionRateData"


class QueryTradingCommissionRateData(BaseModel):
    """Model for the response data of QueryTradingCommissionRate.

    Args:
        taker_commission_rate (float): Taker commission rate.
        maker_commission_rate (float): Maker commission rate.

    """

    taker_commission_rate: float = Field(..., alias="takerCommissionRate")
    maker_commission_rate: float = Field(..., alias="makerCommissionRate")


class SpotCancelAllAfterResponse(BaseModel):
    """Model for the response of CancelAllAfter.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CancelAllAfterData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CancelAllAfterData"


class CancelAllAfterData(BaseModel):
    """Model for the response data of CancelAllAfter.

    Args:
        trigger_time (int): Trigger time for deleting all pending orders.
        status (CancelAllAfterStatus): ACTIVATED (Activation successful)/CLOSED (Closed successfully)/FAILED (Failed).
        note (str): Explanation.

    """

    trigger_time: int = Field(..., alias="triggerTime")
    status: "CancelAllAfterStatus"
    note: str


class CancelAllAfterStatus(str, Enum):
    """Status of cancel all after operation.

    Args:
        ACTIVATED (str): Activation successful.
        CLOSED (str): Closed successfully.
        FAILED (str): Failed.

    """

    ACTIVATED = "ACTIVATED"
    CLOSED = "CLOSED"
    FAILED = "FAILED"


class SpotCancelOrderResponse(BaseModel):
    """Model for the response of CancelOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CancelOrderData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CancelOrderData"


class CancelOrderData(BaseModel):
    """Model for the response data of CancelOrder.

    Args:
        symbol (str): Trading pair.
        order_id (int): Order ID.
        price (str): Price.
        stop_price (str): Trigger price.
        orig_qty (str): Original quantity.
        executed_qty (str): Executed quantity.
        cummulative_quote_qty (str): Cumulative quote asset transacted quantity.
        status (OrderStatus): Order status.
        type (SpotOrderType): Order type.
        side (OrderSide): BUY/SELL.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    price: str
    stop_price: str = Field(..., alias="stopPrice")
    orig_qty: str = Field(..., alias="origQty")
    executed_qty: str = Field(..., alias="executedQty")
    cummulative_quote_qty: str = Field(..., alias="cummulativeQuoteQty")
    status: OrderStatus
    type: SpotOrderType
    side: OrderSide


class SpotCancelMultipleOrdersResponse(BaseModel):
    """Model for the response of CancelMultipleOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CancelMultipleOrdersData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CancelMultipleOrdersData"


class CancelMultipleOrdersData(BaseModel):
    """Model for the response data of CancelMultipleOrders.

    Args:
        fails (List[FailItem]): List of failed orders.
        orders (List[CancelOrderData]): List of successfully canceled orders.

    """

    fails: list["FailItem"]
    orders: list[CancelOrderData]


class FailItem(BaseModel):
    """Model for the failed order item.

    Args:
        order_id (str): Order ID.
        error (str): Error message.

    """

    order_id: str = Field(..., alias="orderId")
    error: str


class SpotCancelAllOpenOrdersResponse(BaseModel):
    """Model for the response of CancelAllOpenOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CancelAllOpenOrdersData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CancelAllOpenOrdersData"


class CancelAllOpenOrdersData(BaseModel):
    """Model for the response data of CancelAllOpenOrders.

    Args:
        orders (List[CancelOrderData]): List of canceled orders.

    """

    orders: list[CancelOrderData]


class CancelReplaceMode(str, Enum):
    """Enum for cancel replace modes.

    Args:
        STOP_ON_FAILURE (str): Stop on failure.
        ALLOW_FAILURE (str): Allow failure.

    """

    STOP_ON_FAILURE = "STOP_ON_FAILURE"
    ALLOW_FAILURE = "ALLOW_FAILURE"


class SpotCancelReplaceOrderResponse(BaseModel):
    """Model for the response of CancelReplaceOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CancelReplaceOrderData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CancelReplaceOrderData"


class CancelReplaceOrderData(BaseModel):
    """Model for the response data of CancelReplaceOrder.

    Args:
        cancel_result (CancelResult): Result of the cancel operation.
        open_result (OpenResult): Result of the open operation.
        order_open_response (OrderOpenResponse): Response for the open order.
        order_cancel_response (OrderCancelResponse): Response for the cancel order.

    """

    cancel_result: "CancelResult" = Field(..., alias="cancelResult")
    open_result: "OpenResult" = Field(..., alias="openResult")
    order_open_response: "OrderOpenResponse" = Field(..., alias="orderOpenResponse")
    order_cancel_response: "OrderCancelResponse" = Field(
        ...,
        alias="orderCancelResponse",
    )


class CancelResult(BaseModel):
    """Model for the cancel result.

    Args:
        code (int): Error code.
        msg (str): Error message.
        result (bool): Result of the cancel operation.

    """

    code: int
    msg: str
    result: bool


class OpenResult(BaseModel):
    """Model for the open result.

    Args:
        code (int): Error code.
        msg (str): Error message.
        result (bool): Result of the open operation.

    """

    code: int
    msg: str
    result: bool


class OrderOpenResponse(BaseModel):
    """Model for the order open response.

    Args:
        symbol (str): Trading symbol.
        order_id (int): Order ID.
        transact_time (int): Transaction timestamp.
        price (str): Order price.
        stop_price (str): Trigger price.
        orig_qty (str): Original quantity.
        executed_qty (str): Executed quantity.
        cummulative_quote_qty (str): Cumulative quote quantity.
        status (OrderStatus): Order status.
        type (SpotOrderType): Order type.
        side (OrderSide): BUY or SELL.
        client_order_id (str): User-defined order ID.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    transact_time: int = Field(..., alias="transactTime")
    price: str
    stop_price: str = Field(..., alias="stopPrice")
    orig_qty: str = Field(..., alias="origQty")
    executed_qty: str = Field(..., alias="executedQty")
    cummulative_quote_qty: str = Field(..., alias="cummulativeQuoteQty")
    status: OrderStatus
    type: SpotOrderType
    side: OrderSide
    client_order_id: str = Field(..., alias="clientOrderID")


class OrderCancelResponse(BaseModel):
    """Model for the order cancel response.

    Args:
        symbol (str): Trading symbol.
        order_id (int): Order ID.
        price (str): Order price.
        stop_price (str): Trigger price.
        orig_qty (str): Original quantity.
        executed_qty (str): Executed quantity.
        cummulative_quote_qty (str): Cumulative quote quantity.
        status (OrderStatus): Order status.
        type (SpotOrderType): Order type.
        side (OrderSide): BUY or SELL.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    price: str
    stop_price: str = Field(..., alias="stopPrice")
    orig_qty: str = Field(..., alias="origQty")
    executed_qty: str = Field(..., alias="executedQty")
    cummulative_quote_qty: str = Field(..., alias="cummulativeQuoteQty")
    status: OrderStatus
    type: SpotOrderType
    side: OrderSide


class QueryTransactionDetailsResponse(BaseModel):
    """Model for the response of QueryTransactionDetails.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (QueryTransactionDetailsData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "QueryTransactionDetailsData"


class QueryTransactionDetailsData(BaseModel):
    """Model for the response data of QueryTransactionDetails.

    Args:
        fills (List[FillItem]): List of trade details.

    """

    fills: list["FillItem"]


class FillItem(BaseModel):
    """Model for the fill item.

    Args:
        symbol (str): Trading symbol.
        id (int): Trade ID.
        order_id (int): Order ID.
        price (str): Price of the trade.
        qty (str): Quantity of the trade.
        quote_qty (str): Quote asset quantity traded.
        commission (float): Commission amount.
        commission_asset (str): Commission asset type.
        time (int): Trade time.
        is_buyer (bool): Whether the buyer.
        is_maker (bool): Whether the maker.

    """

    symbol: str
    id: int
    order_id: int = Field(..., alias="orderId")
    price: str
    qty: str
    quote_qty: str = Field(..., alias="quoteQty")
    commission: float
    commission_asset: str = Field(..., alias="commissionAsset")
    time: int
    is_buyer: bool = Field(..., alias="isBuyer")
    is_maker: bool = Field(..., alias="isMaker")


class CreateOcoOrderResponse(BaseModel):
    """Model for the response of CreateOcoOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (List[OcoOrderItem]): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: list["OcoOrderItem"]


class OcoOrderItem(BaseModel):
    """Model for the OCO order item.

    Args:
        transaction_time (int): Order time.
        order_id (str): Order ID.
        client_order_id (str): User-defined order ID.
        symbol (str): Trading pair.
        order_type (str): OCO order type.
        side (str): BUY or SELL.
        trigger_price (float): Trigger price.
        price (float): Order price.
        quantity (float): Order quantity.
        order_list_id (str): OCO order group ID.
        status (str): Order status.

    """

    transaction_time: int = Field(..., alias="transactionTime")
    order_id: str = Field(..., alias="orderId")
    client_order_id: str = Field(..., alias="clientOrderId")
    symbol: str
    order_type: str = Field(..., alias="spotOrderType")
    side: str
    trigger_price: float = Field(..., alias="triggerPrice")
    price: float
    quantity: float
    order_list_id: str = Field(..., alias="orderListId")
    status: str


class CancelOcoOrderResponse(BaseModel):
    """Model for the response of CancelOcoOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (CancelOcoOrderData): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: "CancelOcoOrderData"


class CancelOcoOrderData(BaseModel):
    """Model for the response data of CancelOcoOrder.

    Args:
        order_id (str): Order ID.
        client_order_id (str): User-defined order ID.

    """

    order_id: str = Field(..., alias="orderId")
    client_order_id: str = Field(..., alias="clientOrderId")


class QueryOcoOrderListResponse(BaseModel):
    """Model for the response of QueryOcoOrderList.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (List[OcoOrderItem]): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: list["OcoOrderItem"]


class QueryAllOpenOcoOrdersResponse(BaseModel):
    """Model for the response of QueryAllOpenOcoOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (List[OcoOrderItem]): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: list["OcoOrderItem"]


class QueryOcoHistoricalOrderListResponse(BaseModel):
    """Model for the response of QueryOcoHistoricalOrderList.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        debug_msg (str): Debug message.
        data (List[OcoOrderItem]): The response data.

    """

    code: int
    msg: str
    debug_msg: str = Field(..., alias="debugMsg")
    data: list["OcoOrderItem"]
