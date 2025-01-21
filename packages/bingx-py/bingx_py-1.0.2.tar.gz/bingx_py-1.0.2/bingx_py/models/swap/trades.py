from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from bingx_py.models.general import OrderSide, OrderStatus, TimeInForce


class OrderType(str, Enum):
    """Enum for order types.

    Args:
        LIMIT (str): Limit order.
        MARKET (str): Market order.
        STOP_MARKET (str): Stop market order.
        TAKE_PROFIT_MARKET (str): Take profit market order.
        STOP (str): Stop order.
        TAKE_PROFIT (str): Take profit order.
        TRIGGER_LIMIT (str): Trigger limit order.
        TRIGGER_MARKET (str): Trigger market order.
        TRAILING_STOP_MARKET (str): Trailing stop market order.
        TRAILING_TP_SL (str): Trailing take profit/stop loss order.

    """

    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    STOP = "STOP"
    TAKE_PROFIT = "TAKE_PROFIT"
    TRIGGER_LIMIT = "TRIGGER_LIMIT"
    TRIGGER_MARKET = "TRIGGER_MARKET"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"
    TRAILING_TP_SL = "TRAILING_TP_SL"


class PositionSide(str, Enum):
    """Enum for position sides.

    Args:
        BOTH (str): Both long and short positions.
        LONG (str): Long position.
        SHORT (str): Short position.

    """

    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"


class WorkingType(str, Enum):
    """Enum for working types.

    Args:
        MARK_PRICE (str): Order is based on the mark price.
        CONTRACT_PRICE (str): Order is based on the contract price.
        INDEX_PRICE (str): Order is based on the index price.

    """

    MARK_PRICE = "MARK_PRICE"
    CONTRACT_PRICE = "CONTRACT_PRICE"
    INDEX_PRICE = "INDEX_PRICE"


class OrderRequest(BaseModel):
    """Model for an individual order in the batch.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        type (OrderType): Order type.
        side (OrderSide): BUY or SELL.
        position_side (Optional[PositionSide]): Position direction (BOTH, LONG, SHORT). Defaults to None.
        reduce_only (Optional[bool]): true or false. Defaults to None.
        price (Optional[float]): Price or trailing stop distance. Defaults to None.
        quantity (Optional[float]): Original quantity. Defaults to None.
        stop_price (Optional[float]): Trigger price. Defaults to None.
        price_rate (Optional[float]): For TRAILING_STOP_MARKET or TRAILING_TP_SL. Maximum: 1. Defaults to None.
        stop_loss (Optional[str]): Stop loss settings. Defaults to None.
        take_profit (Optional[str]): Take profit settings. Defaults to None.
        working_type (Optional[WorkingType]): StopPrice trigger price types. Defaults to None.
        client_order_id (Optional[str]): Customized order ID. Defaults to None.
        time_in_force (Optional[TimeInForce]): Time in force. Defaults to None.
        close_position (Optional[bool]): true or false. Defaults to None.
        activation_price (Optional[float]): Activation price for TRAILING_STOP_MARKET or TRAILING_TP_SL. Defaults to None.
        stop_guaranteed (Optional[bool]): true or false. Defaults to None.

    """

    symbol: str
    type: OrderType
    side: OrderSide
    position_side: Optional[PositionSide] = Field(
        None,
        serialization_alias="positionSide",
    )
    reduce_only: Optional[bool] = Field(None, serialization_alias="reduceOnly")
    price: Optional[float] = None
    quantity: Optional[float] = None
    stop_price: Optional[float] = Field(None, serialization_alias="stopPrice")
    price_rate: Optional[float] = Field(None, serialization_alias="priceRate")
    stop_loss: Optional[str] = Field(None, serialization_alias="stopLoss")
    take_profit: Optional[str] = Field(None, serialization_alias="takeProfit")
    working_type: Optional[WorkingType] = Field(None, serialization_alias="workingType")
    client_order_id: Optional[str] = Field(None, serialization_alias="clientOrderId")
    time_in_force: Optional[TimeInForce] = Field(
        None,
        serialization_alias="timeInForce",
    )
    close_position: Optional[bool] = Field(None, serialization_alias="closePosition")
    activation_price: Optional[float] = Field(
        None,
        serialization_alias="activationPrice",
    )
    stop_guaranteed: Optional[bool] = Field(None, serialization_alias="stopGuaranteed")


class TestOrderResponse(BaseModel):
    """Model for the response of TestOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (TestOrderData): The response data.

    """

    code: int
    msg: str
    data: "TestOrderData"


class TestOrderData(BaseModel):
    """Model for the response data of TestOrder.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        order_id (int): Order ID.
        side (OrderSide): BUY or SELL.
        position_side (PositionSide): Position direction (BOTH, LONG, SHORT).
        type (OrderType): Order type.
        client_order_id (str): Customized order ID.
        working_type (WorkingType): Working type, e.g., MARK_PRICE.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    client_order_id: str = Field(..., alias="clientOrderId")
    working_type: WorkingType = Field(..., alias="workingType")


class PlaceOrderInDemoTradingResponse(BaseModel):
    """Model for the response of PlaceOrderInDemoTrading.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (PlaceOrderInDemoTradingData): The response data.

    """

    code: int
    msg: str
    data: "PlaceOrderInDemoTradingData"


class PlaceOrderInDemoTradingData(BaseModel):
    """Model for the response data of PlaceOrderInDemoTrading.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        order_id (int): Order ID.
        side (OrderSide): BUY or SELL.
        position_side (PositionSide): Position direction (BOTH, LONG, SHORT).
        type (OrderType): Order type.
        client_order_id (str): Customized order ID.
        working_type (WorkingType): Working type, e.g., MARK_PRICE.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    client_order_id: str = Field(..., alias="clientOrderId")
    working_type: WorkingType = Field(..., alias="workingType")


class PlaceOrderResponse(BaseModel):
    """Model for the response of PlaceOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (PlaceOrderData): The response data.

    """

    code: int
    msg: str
    data: "PlaceOrderData"


class PlaceOrderData(BaseModel):
    """Model for the response data of PlaceOrder.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        order_id (int): Order ID.
        side (OrderSide): BUY or SELL.
        position_side (PositionSide): Position direction (BOTH, LONG, SHORT).
        type (OrderType): Order type.
        client_order_id (str): Customized order ID.
        working_type (WorkingType): Working type, e.g., MARK_PRICE.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    client_order_id: str = Field(..., alias="clientOrderId")
    working_type: WorkingType = Field(..., alias="workingType")


class PlaceMultipleOrdersResponse(BaseModel):
    """Model for the response of PlaceMultipleOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (PlaceMultipleOrdersData): The response data.

    """

    code: int
    msg: str
    data: "PlaceMultipleOrdersData"


class PlaceMultipleOrdersData(BaseModel):
    """Model for the response data of PlaceMultipleOrders.

    Args:
        orders (List[OrderResponse]): List of order responses.

    """

    orders: list["OrderResponse"]


class OrderResponse(BaseModel):
    """Model for the response of a single order.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        order_id (int): Order ID.
        side (OrderSide): BUY or SELL.
        position_side (PositionSide): Position direction (BOTH, LONG, SHORT).
        type (OrderType): Order type.
        client_order_id (str): Customized order ID.
        working_type (WorkingType): Working type, e.g., MARK_PRICE.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    client_order_id: str = Field(..., alias="clientOrderId")
    working_type: WorkingType = Field(..., alias="workingType")


class CloseAllPositionsResponse(BaseModel):
    """Model for the response of CloseAllPositions.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CloseAllPositionsData): The response data.

    """

    code: int
    msg: str
    data: "CloseAllPositionsData"


class CloseAllPositionsData(BaseModel):
    """Model for the response data of CloseAllPositions.

    Args:
        success (List[int]): List of successful order IDs.
        failed (Optional[List[int]]): List of failed order IDs. Defaults to None.

    """

    success: list[int]
    failed: Optional[list[int]] = None


class CancelOrderResponse(BaseModel):
    """Model for the response of CancelOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CancelOrderData): The response data.

    """

    code: int
    msg: str
    data: "CancelOrderData"


class CancelOrderData(BaseModel):
    """Model for the response data of CancelOrder.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        order_id (int): Order ID.
        side (OrderSide): BUY or SELL.
        position_side (PositionSide): Position direction (BOTH, LONG, SHORT).
        type (OrderType): Order type.
        orig_qty (str): Original quantity.
        price (str): Price.
        executed_qty (str): Executed quantity.
        avg_price (str): Average transaction price.
        cum_quote (str): Transaction amount.
        stop_price (str): Trigger price.
        profit (str): Profit and loss.
        commission (str): Fee.
        status (OrderStatus): Order status.
        time (int): Order time, unit: millisecond.
        update_time (int): Update time, unit: millisecond.
        client_order_id (str): Customized order ID.
        leverage (str): Leverage.
        take_profit (Dict[str, Any]): Take profit settings.
        stop_loss (Dict[str, Any]): Stop loss settings.
        advance_attr (int): Advanced attributes.
        position_id (int): Position ID.
        take_profit_entrust_price (int): Take profit entrust price.
        stop_loss_entrust_price (int): Stop loss entrust price.
        order_type (str): Order type.
        working_type (WorkingType): Working type.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    orig_qty: str = Field(..., alias="origQty")
    price: str
    executed_qty: str = Field(..., alias="executedQty")
    avg_price: str = Field(..., alias="avgPrice")
    cum_quote: str = Field(..., alias="cumQuote")
    stop_price: str = Field(..., alias="stopPrice")
    profit: str
    commission: str
    status: OrderStatus
    time: int
    update_time: int = Field(..., alias="updateTime")
    client_order_id: str = Field(..., alias="clientOrderId")
    leverage: str
    take_profit: dict[str, Any] = Field(..., alias="takeProfit")
    stop_loss: dict[str, Any] = Field(..., alias="stopLoss")
    advance_attr: int = Field(..., alias="advanceAttr")
    position_id: int = Field(..., alias="positionID")
    take_profit_entrust_price: int = Field(..., alias="takeProfitEntrustPrice")
    stop_loss_entrust_price: int = Field(..., alias="stopLossEntrustPrice")
    order_type: str = Field(..., alias="orderType")
    working_type: WorkingType = Field(..., alias="workingType")


class CancelMultipleOrdersResponse(BaseModel):
    """Model for the response of CancelMultipleOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CancelMultipleOrdersData): The response data.

    """

    code: int
    msg: str
    data: "CancelMultipleOrdersData"


class CancelMultipleOrdersData(BaseModel):
    """Model for the response data of CancelMultipleOrders.

    Args:
        success (List[CancelOrderData]): List of successfully canceled orders.
        failed (Optional[List[FailedOrder]]): List of failed orders. Defaults to None.

    """

    success: list[CancelOrderData]
    failed: Optional[list["FailedOrder"]] = None


class FailedOrder(BaseModel):
    """Model for a failed order.

    Args:
        order_id (int): Order ID.
        client_order_id (str): Customized order ID.
        error_code (int): Error code.
        error_message (str): Error message.

    """

    order_id: int = Field(..., alias="orderId")
    client_order_id: str = Field(..., alias="clientOrderId")
    error_code: int = Field(..., alias="errorCode")
    error_message: str = Field(..., alias="errorMessage")


class CancelAllOpenOrdersResponse(BaseModel):
    """Model for the response of CancelAllOpenOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CancelAllOpenOrdersData): The response data.

    """

    code: int
    msg: str
    data: "CancelAllOpenOrdersData"


class CancelAllOpenOrdersData(BaseModel):
    """Model for the response data of CancelAllOpenOrders.

    Args:
        success (List[CancelOrderData]): List of successfully canceled orders.
        failed (Optional[List[FailedOrder]]): List of failed orders. Defaults to None.

    """

    success: list[CancelOrderData]
    failed: Optional[list[FailedOrder]] = None


class CurrentAllOpenOrdersResponse(BaseModel):
    """Model for the response of CurrentAllOpenOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CurrentAllOpenOrdersData): The response data.

    """

    code: int
    msg: str
    data: "CurrentAllOpenOrdersData"


class CurrentAllOpenOrdersData(BaseModel):
    """Model for the response data of CurrentAllOpenOrders.

    Args:
        orders (List[CancelOrderData]): List of open orders.

    """

    orders: list[CancelOrderData]


class QueryPendingOrderStatusResponse(BaseModel):
    """Model for the response of QueryPendingOrderStatus.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryPendingOrderStatusData): The response data.

    """

    code: int
    msg: str
    data: "QueryPendingOrderStatusData"


class QueryPendingOrderStatusData(BaseModel):
    """Model for the response data of QueryPendingOrderStatus.

    Args:
        order (CancelOrderData): The order data.

    """

    order: CancelOrderData


class TakeProfitStopLoss(BaseModel):
    """Model for Take Profit and Stop Loss details.

    Args:
        type (str): Type of the order.
        quantity (float): Quantity.
        stop_price (float): Stop price.
        price (float): Price.
        working_type (str): Working type.

    """

    type: str
    quantity: float
    stop_price: float = Field(..., alias="stopPrice")
    price: float
    working_type: str = Field(..., alias="workingType")


class QueryOrderDetailsResponse(BaseModel):
    """Model for the response of QueryOrderDetails.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryOrderDetailsData): The response data.

    """

    code: int
    msg: str
    data: "QueryOrderDetailsData"


class QueryOrderDetailsData(BaseModel):
    """Model for the response data of QueryOrderDetails.

    Args:
        order (OrderDetails): Details of the order.

    """

    order: "OrderDetails"


class OrderDetails(BaseModel):
    """Model for the order details.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        order_id (int): Order ID.
        side (OrderSide): BUY/SELL.
        position_side (PositionSide): Position direction (LONG, SHORT, BOTH).
        type (OrderType): Order type (LIMIT, MARKET, etc.).
        orig_qty (str): Original quantity.
        price (str): Price.
        executed_qty (str): Executed quantity.
        avg_price (str): Average price.
        cum_quote (str): Transaction amount.
        stop_price (str): Trigger price.
        profit (str): Profit and loss.
        commission (str): Fee.
        status (OrderStatus): Order status.
        time (int): Order time, unit: millisecond.
        update_time (int): Update time, unit: millisecond.
        client_order_id (str): Customized order ID for users.
        leverage (str): Leverage.
        take_profit (TakeProfitStopLoss): Take profit details.
        stop_loss (TakeProfitStopLoss): Stop loss details.
        advance_attr (int): Advanced attributes.
        position_id (int): Position ID.
        take_profit_entrust_price (float): Take profit entrust price.
        stop_loss_entrust_price (float): Stop loss entrust price.
        order_type (str): Order type.
        working_type (WorkingType): StopPrice trigger price types.
        stop_guaranteed (bool): Whether the guaranteed stop-loss feature is enabled.
        trigger_order_id (int): Trigger order ID associated with this order.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    orig_qty: str = Field(..., alias="origQty")
    price: str
    executed_qty: str = Field(..., alias="executedQty")
    avg_price: str = Field(..., alias="avgPrice")
    cum_quote: str = Field(..., alias="cumQuote")
    stop_price: str = Field(..., alias="stopPrice")
    profit: str
    commission: str
    status: OrderStatus
    time: int
    update_time: int = Field(..., alias="updateTime")
    client_order_id: str = Field(..., alias="clientOrderId")
    leverage: str
    take_profit: TakeProfitStopLoss = Field(..., alias="takeProfit")
    stop_loss: TakeProfitStopLoss = Field(..., alias="stopLoss")
    advance_attr: int = Field(..., alias="advanceAttr")
    position_id: int = Field(..., alias="positionID")
    take_profit_entrust_price: float = Field(..., alias="takeProfitEntrustPrice")
    stop_loss_entrust_price: float = Field(..., alias="stopLossEntrustPrice")
    order_type: str = Field(..., alias="orderType")
    working_type: WorkingType = Field(..., alias="workingType")
    stop_guaranteed: bool = Field(..., alias="stopGuaranteed")
    trigger_order_id: int = Field(..., alias="triggerOrderId")


class MarginType(str, Enum):
    """Margin type.

    Args:
        ISOLATED: Isolated margin mode.
        CROSSED: Crossed margin mode.

    """

    ISOLATED = "ISOLATED"
    CROSSED = "CROSSED"


class QueryMarginTypeResponse(BaseModel):
    """Model for the response of QueryMarginType.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryMarginTypeData): The response data.

    """

    code: int
    msg: str
    data: "QueryMarginTypeData"


class QueryMarginTypeData(BaseModel):
    """Model for the response data of QueryMarginType.

    Args:
        margin_type (MarginType): Margin mode (ISOLATED or CROSSED).

    """

    margin_type: MarginType = Field(..., alias="marginType")


class ChangeMarginTypeResponse(BaseModel):
    """Model for the response of ChangeMarginType.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.

    """

    code: int
    msg: str


class QueryLeverageAndAvailablePositionsResponse(BaseModel):
    """Model for the response of QueryLeverageAndAvailablePositions.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryLeverageAndAvailablePositionsData): The response data.

    """

    code: int
    msg: str
    data: "QueryLeverageAndAvailablePositionsData"


class QueryLeverageAndAvailablePositionsData(BaseModel):
    """Model for the response data of QueryLeverageAndAvailablePositions.

    Args:
        long_leverage (int): Long position leverage.
        short_leverage (int): Short position leverage.
        max_long_leverage (int): Max Long position leverage.
        max_short_leverage (int): Max Short position leverage.
        available_long_vol (str): Available Long Volume.
        available_short_vol (str): Available Short Volume.
        available_long_val (str): Available Long Value.
        available_short_val (str): Available Short Value.
        max_position_long_val (str): Maximum Position Long Value.
        max_position_short_val (str): Maximum Position Short Value.

    """

    long_leverage: int = Field(..., alias="longLeverage")
    short_leverage: int = Field(..., alias="shortLeverage")
    max_long_leverage: int = Field(..., alias="maxLongLeverage")
    max_short_leverage: int = Field(..., alias="maxShortLeverage")
    available_long_vol: str = Field(..., alias="availableLongVol")
    available_short_vol: str = Field(..., alias="availableShortVol")
    available_long_val: str = Field(..., alias="availableLongVal")
    available_short_val: str = Field(..., alias="availableShortVal")
    max_position_long_val: str = Field(..., alias="maxPositionLongVal")
    max_position_short_val: str = Field(..., alias="maxPositionShortVal")


class SetLeverageResponse(BaseModel):
    """Model for the response of SetLeverage.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (SetLeverageData): The response data.

    """

    code: int
    msg: str
    data: "SetLeverageData"


class SetLeverageData(BaseModel):
    """Model for the response data of SetLeverage.

    Args:
        leverage (int): Leverage value.
        symbol (str): Trading pair.
        available_long_vol (str): Available Long Volume.
        available_short_vol (str): Available Short Volume.
        available_long_val (str): Available Long Value.
        available_short_val (str): Available Short Value.
        max_position_long_val (str): Maximum Position Long Value.
        max_position_short_val (str): Maximum Position Short Value.

    """

    leverage: int
    symbol: str
    available_long_vol: str = Field(..., alias="availableLongVol")
    available_short_vol: str = Field(..., alias="availableShortVol")
    available_long_val: str = Field(..., alias="availableLongVal")
    available_short_val: str = Field(..., alias="availableShortVal")
    max_position_long_val: str = Field(..., alias="maxPositionLongVal")
    max_position_short_val: str = Field(..., alias="maxPositionShortVal")


class UsersForceOrdersResponse(BaseModel):
    """Model for the response of users' force orders.

    Args:
        code (int): Response code.
        msg (str): Response message.
        data (UsersForceOrdersData): The response data containing force orders.

    """

    code: int
    msg: str
    data: "UsersForceOrdersData"


class UsersForceOrdersData(BaseModel):
    """Model for the data of users' force orders.

    Args:
        orders (List[OrderDetails]): List of force order details.

    """

    orders: list["OrderDetails"]


class SwapQueryOrderHistoryResponse(BaseModel):
    """Model for the response of querying order history.

    Args:
        code (int): Response code.
        msg (str): Response message.
        data (SwapQueryOrderHistoryData): The response data containing historical orders.

    """

    code: int
    msg: str
    data: "SwapQueryOrderHistoryData"


class SwapQueryOrderHistoryData(BaseModel):
    """Model for the data of querying order history.

    Args:
        orders (List[SwapHistoryOrderDetails]): List of historical order details.

    """

    orders: list["SwapHistoryOrderDetails"]


class ModifyIsolatedPositionMarginResponse(BaseModel):
    """Model for the response of modifying isolated position margin.

    Args:
        code (int): Response code.
        msg (str): Response message.
        amount (float): The amount of margin modified.
        type (int): The type of margin modification.

    """

    code: int
    msg: str
    amount: float
    type: int


class QueryHistoricalTransactionOrdersResponse(BaseModel):
    """Model for the response of querying historical transaction orders.

    Args:
        code (int): Response code.
        msg (str): Response message.
        data (QueryHistoricalTransactionOrdersData): The response data containing historical transaction orders.

    """

    code: int
    msg: str
    data: "QueryHistoricalTransactionOrdersData"


class QueryHistoricalTransactionOrdersData(BaseModel):
    """Model for the data of querying historical transaction orders.

    Args:
        fill_orders (List[FillOrderDetails]): List of filled order details.

    """

    fill_orders: list["FillOrderDetails"] = Field(..., alias="fill_orders")


class SetPositionModeResponse(BaseModel):
    """Model for the response of setting position mode.

    Args:
        code (int): Response code.
        msg (str): Response message.
        data (SetPositionModeData): The response data containing position mode information.

    """

    code: int
    msg: str
    data: "SetPositionModeData"


class SetPositionModeData(BaseModel):
    """Model for the data of setting position mode.

    Args:
        dual_side_position (str): Indicates whether dual-side position mode is enabled.

    """

    dual_side_position: str = Field(..., alias="dualSidePosition")


class QueryPositionModeResponse(BaseModel):
    """Model for the response of querying position mode.

    Args:
        code (int): Response code.
        msg (str): Response message.
        data (QueryPositionModeData): The response data containing position mode information.

    """

    code: int
    msg: str
    data: "QueryPositionModeData"


class QueryPositionModeData(BaseModel):
    """Model for the data of querying position mode.

    Args:
        dual_side_position (str): Indicates whether dual-side position mode is enabled.

    """

    dual_side_position: str = Field(..., alias="dualSidePosition")


class SwapHistoryOrderDetails(BaseModel):
    """Model for historical order details.

    Args:
        symbol (str): Trading symbol.
        order_id (int): Order ID.
        side (OrderSide): Order side (BUY/SELL).
        position_side (PositionSide): Position side (LONG/SHORT).
        type (OrderType): Order type (LIMIT, MARKET, etc.).
        orig_qty (str): Original quantity.
        price (str): Order price.
        executed_qty (str): Executed quantity.
        avg_price (str): Average price.
        cum_quote (str): Cumulative quote asset transacted.
        stop_price (str): Stop price.
        profit (str): Profit.
        commission (str): Commission.
        status (OrderStatus): Order status.
        time (int): Order creation time.
        update_time (int): Order update time.
        client_order_id (str): Client order ID.
        leverage (str): Leverage used.
        take_profit (TakeProfitStopLoss): Take profit details.
        stop_loss (TakeProfitStopLoss): Stop loss details.
        advance_attr (int): Advanced attributes.
        position_id (int): Position ID.
        take_profit_entrust_price (float): Take profit entrust price.
        stop_loss_entrust_price (float): Stop loss entrust price.
        order_type (str): Order type.
        working_type (WorkingType): Working type (MARK_PRICE, CONTRACT_PRICE).
        stop_guaranteed (bool): Whether stop loss is guaranteed.
        trigger_order_id (int): Trigger order ID.

    """

    symbol: str
    order_id: int = Field(..., alias="orderId")
    side: OrderSide
    position_side: PositionSide = Field(..., alias="positionSide")
    type: OrderType
    orig_qty: str = Field(..., alias="origQty")
    price: str
    executed_qty: str = Field(..., alias="executedQty")
    avg_price: str = Field(..., alias="avgPrice")
    cum_quote: str = Field(..., alias="cumQuote")
    stop_price: str = Field(..., alias="stopPrice")
    profit: str
    commission: str
    status: OrderStatus
    time: int
    update_time: int = Field(..., alias="updateTime")
    client_order_id: str = Field(..., alias="clientOrderId")
    leverage: str
    take_profit: TakeProfitStopLoss = Field(..., alias="takeProfit")
    stop_loss: TakeProfitStopLoss = Field(..., alias="stopLoss")
    advance_attr: int = Field(..., alias="advanceAttr")
    position_id: int = Field(..., alias="positionID")
    take_profit_entrust_price: float = Field(..., alias="takeProfitEntrustPrice")
    stop_loss_entrust_price: float = Field(..., alias="stopLossEntrustPrice")
    order_type: str = Field(..., alias="orderType")
    working_type: WorkingType = Field(..., alias="workingType")
    stop_guaranteed: bool = Field(..., alias="stopGuaranteed")
    trigger_order_id: int = Field(..., alias="triggerOrderId")


class FillOrderDetails(BaseModel):
    """Model for filled order details.

    Args:
        filled_tm (str): Filled timestamp.
        volume (str): Filled volume.
        price (str): Filled price.
        amount (str): Filled amount.
        commission (str): Commission.
        currency (str): Currency.
        order_id (str): Order ID.
        liquidated_price (str): Liquidated price.
        liquidated_margin_ratio (str): Liquidated margin ratio.
        filled_time (str): Filled time.
        client_order_id (str): Client order ID.
        symbol (str): Trading symbol.

    """

    filled_tm: str = Field(..., alias="filledTm")
    volume: str
    price: str
    amount: str
    commission: str
    currency: str
    order_id: str = Field(..., alias="orderId")
    liquidated_price: str = Field(..., alias="liquidatedPrice")
    liquidated_margin_ratio: str = Field(..., alias="liquidatedMarginRatio")
    filled_time: str = Field(..., alias="filledTime")
    client_order_id: str = Field(..., alias="clientOrderId")
    symbol: str


class CancelReplaceOrderResponse(BaseModel):
    """Model for the response of CancelReplaceOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CancelReplaceOrderData): The response data.

    """

    code: int
    msg: str
    data: "CancelReplaceOrderData"


class CancelReplaceOrderData(BaseModel):
    """Model for the response data of CancelReplaceOrder.

    Args:
        cancel_result (str): Cancellation result.
        cancel_msg (str): Cancellation message.
        cancel_response (OrderDetails): Details of the canceled order.
        replace_result (str): Replacement result.
        replace_msg (str): Replacement message.
        new_order_response (OrderDetails): Details of the new order.

    """

    cancel_result: str = Field(..., alias="cancelResult")
    cancel_msg: str = Field(..., alias="cancelMsg")
    cancel_response: "OrderDetails" = Field(..., alias="cancelResponse")
    replace_result: str = Field(..., alias="replaceResult")
    replace_msg: str = Field(..., alias="replaceMsg")
    new_order_response: "OrderDetails" = Field(..., alias="newOrderResponse")


class BatchCancelReplaceOrdersResponse(BaseModel):
    """Model for the response of BatchCancelReplaceOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[CancelReplaceOrderData]): The response data.

    """

    code: int
    msg: str
    data: list["CancelReplaceOrderData"]


class CancelAllAfterResponse(BaseModel):
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
        trigger_time (int): Trigger time for canceling orders.
        status (str): Status of the operation.
        note (str): Explanation of the operation.

    """

    trigger_time: int = Field(..., alias="triggerTime")
    status: str
    note: str


class ClosePositionResponse(BaseModel):
    """Model for the response of ClosePosition.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Timestamp of the response.
        data (ClosePositionData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "ClosePositionData"


class ClosePositionData(BaseModel):
    """Model for the response data of ClosePosition.

    Args:
        order_id (int): Order ID.
        position_id (str): Position ID.
        symbol (str): Trading pair.
        side (str): BUY or SELL.
        type (str): Order type.
        position_side (str): LONG, SHORT, or BOTH.
        orig_qty (str): Original quantity.

    """

    order_id: int = Field(..., alias="orderId")
    position_id: str = Field(..., alias="positionId")
    symbol: str
    side: str
    type: str
    position_side: str = Field(..., alias="positionSide")
    orig_qty: str = Field(..., alias="origQty")


class QueryAllOrdersResponse(BaseModel):
    """Model for the response of QueryAllOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryAllOrdersData): The response data.

    """

    code: int
    msg: str
    data: "QueryAllOrdersData"


class QueryAllOrdersData(BaseModel):
    """Model for the response data of QueryAllOrders.

    Args:
        orders (List[OrderDetails]): List of orders.

    """

    orders: list["OrderDetails"]


class CancelReplaceOrderRequest(BaseModel):
    """Model for the request of CancelReplaceOrder.

    Args:
        cancel_replace_mode (str): STOP_ON_FAILURE or ALLOW_FAILURE.
        symbol (str): Trading pair, e.g., BTC-USDT.
        type (str): Order type.
        side (str): BUY or SELL.
        position_side (str): LONG, SHORT, or BOTH.
        cancel_client_order_id (Optional[str]): Client-defined order ID to cancel. Defaults to None.
        cancel_order_id (Optional[int]): Platform order ID to cancel. Defaults to None.
        cancel_restrictions (Optional[str]): ONLY_NEW, ONLY_PENDING, or ONLY_PARTIALLY_FILLED. Defaults to None.
        reduce_only (Optional[bool]): Whether the order is reduce-only. Defaults to None.
        price (Optional[float]): Order price. Defaults to None.
        quantity (Optional[float]): Order quantity. Defaults to None.
        stop_price (Optional[float]): Trigger price. Defaults to None.
        price_rate (Optional[float]): Price rate for TRAILING_STOP_MARKET or TRAILING_TP_SL. Defaults to None.
        working_type (Optional[str]): MARK_PRICE, CONTRACT_PRICE, or INDEX_PRICE. Defaults to None.
        stop_loss (Optional[str]): Stop loss settings. Defaults to None.
        take_profit (Optional[str]): Take profit settings. Defaults to None.
        client_order_id (Optional[str]): Custom client order ID. Defaults to None.
        close_position (Optional[bool]): Whether to close the position. Defaults to None.
        activation_price (Optional[float]): Activation price for TRAILING_STOP_MARKET or TRAILING_TP_SL. Defaults to None.
        stop_guaranteed (Optional[bool]): true or false. Defaults to None.
        time_in_force (Optional[str]): Time in force. Defaults to None.
        recv_window (Optional[int]): Request valid time window (milliseconds). Defaults to None.

    """

    cancel_replace_mode: str = Field(..., serialization_alias="cancelReplaceMode")
    symbol: str
    type: str
    side: str
    position_side: str = Field(..., serialization_alias="positionSide")
    cancel_client_order_id: Optional[str] = Field(
        None,
        serialization_alias="cancelClientOrderId",
    )
    cancel_order_id: Optional[int] = Field(None, serialization_alias="cancelOrderId")
    cancel_restrictions: Optional[str] = Field(
        None,
        serialization_alias="cancelRestrictions",
    )
    reduce_only: Optional[bool] = Field(None, serialization_alias="reduceOnly")
    price: Optional[float] = None
    quantity: Optional[float] = None
    stop_price: Optional[float] = Field(None, serialization_alias="stopPrice")
    price_rate: Optional[float] = Field(None, serialization_alias="priceRate")
    working_type: Optional[str] = Field(None, serialization_alias="workingType")
    stop_loss: Optional[str] = Field(None, serialization_alias="stopLoss")
    take_profit: Optional[str] = Field(None, serialization_alias="takeProfit")
    client_order_id: Optional[str] = Field(None, serialization_alias="clientOrderId")
    close_position: Optional[bool] = Field(None, serialization_alias="closePosition")
    activation_price: Optional[float] = Field(
        None,
        serialization_alias="activationPrice",
    )
    stop_guaranteed: Optional[bool] = Field(None, serialization_alias="stopGuaranteed")
    time_in_force: Optional[str] = Field(None, serialization_alias="timeInForce")
    recv_window: Optional[int] = Field(None, serialization_alias="recvWindow")


class PositionAndMaintenanceMarginRatioResponse(BaseModel):
    """Model for the response of PositionAndMaintenanceMarginRatio.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (List[PositionAndMaintenanceMarginRatioData]): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: list["PositionAndMaintenanceMarginRatioData"]


class PositionAndMaintenanceMarginRatioData(BaseModel):
    """Model for the response data of PositionAndMaintenanceMarginRatio.

    Args:
        tier (str): Layer.
        symbol (str): Trading pair.
        min_position_val (str): Minimum position value.
        max_position_val (str): Maximum position value.
        maint_margin_ratio (str): Maintenance margin ratio.
        maint_amount (str): Maintenance margin quick calculation amount.

    """

    tier: str
    symbol: str
    min_position_val: str = Field(..., alias="minPositionVal")
    max_position_val: str = Field(..., alias="maxPositionVal")
    maint_margin_ratio: str = Field(..., alias="maintMarginRatio")
    maint_amount: str = Field(..., alias="maintAmount")


class QueryHistoricalTransactionDetailsResponse(BaseModel):
    """Model for the response of QueryHistoricalTransactionDetails.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryHistoricalTransactionDetailsData): The response data.

    """

    code: int
    msg: str
    data: "QueryHistoricalTransactionDetailsData"


class QueryHistoricalTransactionDetailsData(BaseModel):
    """Model for the response data of QueryHistoricalTransactionDetails.

    Args:
        fill_history_orders (List[FillHistoryOrder]): List of historical transaction orders.
        total (int): Total records.

    """

    fill_history_orders: list["FillHistoryOrder"] = Field(
        ...,
        alias="fill_history_orders",
    )
    total: int


class FillHistoryOrder(BaseModel):
    """Model for a historical transaction order.

    Args:
        filled_tm (str): Transaction time.
        volume (str): Transaction quantity.
        price (str): Transaction price.
        qty (str): Transaction quantity.
        quote_qty (str): Transaction amount.
        commission (str): Commission.
        commission_asset (str): Asset unit, usually USDT.
        order_id (str): Order ID.
        trade_id (str): Trade ID.
        filled_time (str): Match the transaction time.
        symbol (str): Trading pair.
        role (str): Active selling and buying, taker: active buying, maker: active selling.
        side (str): Buying and selling direction.
        position_side (str): Position direction.

    """

    filled_tm: str = Field(..., alias="filledTm")
    volume: str
    price: str
    qty: str
    quote_qty: str = Field(..., alias="quoteQty")
    commission: str
    commission_asset: str = Field(..., alias="commissionAsset")
    order_id: str = Field(..., alias="orderId")
    trade_id: str = Field(..., alias="tradeId")
    filled_time: str = Field(..., alias="filledTime")
    symbol: str
    role: str
    side: str
    position_side: str = Field(..., alias="positionSide")


class QueryPositionHistoryResponse(BaseModel):
    """Model for the response of QueryPositionHistory.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[PositionHistoryData]): The response data.

    """

    code: int
    msg: str
    data: list["PositionHistoryData"]


class PositionHistoryData(BaseModel):
    """Model for the response data of QueryPositionHistory.

    Args:
        position_id (str): Position ID.
        symbol (str): Trading pair.
        isolated (bool): Isolated mode.
        position_side (str): Position side LONG/SHORT.
        open_time (int): Open time.
        update_time (int): Update time.
        avg_price (str): Average open price.
        avg_close_price (float): Average close price.
        realised_profit (str): Realized profit and loss.
        net_profit (str): Net profit and loss.
        position_amt (str): Position amount.
        close_position_amt (str): Closed position amount.
        leverage (int): Leverage.
        close_all_positions (bool): All positions closed.
        position_commission (str): Commission fee.
        total_funding (str): Funding fee.

    """

    position_id: str = Field(..., alias="positionId")
    symbol: str
    isolated: bool
    position_side: str = Field(..., alias="positionSide")
    open_time: int = Field(..., alias="openTime")
    update_time: int = Field(..., alias="updateTime")
    avg_price: str = Field(..., alias="avgPrice")
    avg_close_price: float = Field(..., alias="avgClosePrice")
    realised_profit: str = Field(..., alias="realisedProfit")
    net_profit: str = Field(..., alias="netProfit")
    position_amt: str = Field(..., alias="positionAmt")
    close_position_amt: str = Field(..., alias="closePositionAmt")
    leverage: int
    close_all_positions: bool = Field(..., alias="closeAllPositions")
    position_commission: str = Field(..., alias="positionCommission")
    total_funding: str = Field(..., alias="totalFunding")


class IsolatedMarginChangeHistoryResponse(BaseModel):
    """Model for the response of IsolatedMarginChangeHistory.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (IsolatedMarginChangeHistoryData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "IsolatedMarginChangeHistoryData"


class IsolatedMarginChangeHistoryData(BaseModel):
    """Model for the response data of IsolatedMarginChangeHistory.

    Args:
        records (List[IsolatedMarginChangeRecord]): List of margin change records.
        total (int): Total records.

    """

    records: list["IsolatedMarginChangeRecord"]
    total: int


class IsolatedMarginChangeRecord(BaseModel):
    """Model for a margin change record.

    Args:
        symbol (str): Trading pair.
        position_id (str): Position ID.
        change_reason (str): Reason for the margin change.
        margin_change (str): Change amount.
        margin_after_change (str): Total amount after change.
        time (int): Change time.

    """

    symbol: str
    position_id: str = Field(..., alias="positionId")
    change_reason: str = Field(..., alias="changeReason")
    margin_change: str = Field(..., alias="marginChange")
    margin_after_change: str = Field(..., alias="marginAfterChange")
    time: int


class ApplyVstResponse(BaseModel):
    """Model for the response of ApplyVst.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (ApplyVstData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "ApplyVstData"


class ApplyVstData(BaseModel):
    """Model for the response data of ApplyVst.

    Args:
        amount (float): Amount of VST applied.

    """

    amount: float


class PlaceTwapOrderResponse(BaseModel):
    """Model for the response of PlaceTwapOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (PlaceTwapOrderData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "PlaceTwapOrderData"


class PlaceTwapOrderData(BaseModel):
    """Model for the response data of PlaceTwapOrder.

    Args:
        main_order_id (str): TWAP order number.

    """

    main_order_id: str = Field(..., alias="mainOrderId")


class QueryTwapEntrustedOrderResponse(BaseModel):
    """Model for the response of QueryTwapEntrustedOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (QueryTwapEntrustedOrderData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "QueryTwapEntrustedOrderData"


class QueryTwapEntrustedOrderData(BaseModel):
    """Model for the response data of QueryTwapEntrustedOrder.

    Args:
        list (List[TwapOrder]): List of TWAP orders.
        total (int): Total records.

    """

    list: list["TwapOrder"]
    total: int


class QueryTwapHistoricalOrdersResponse(BaseModel):
    """Model for the response of QueryTwapHistoricalOrders.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (QueryTwapHistoricalOrdersData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "QueryTwapHistoricalOrdersData"


class QueryTwapHistoricalOrdersData(BaseModel):
    """Model for the response data of QueryTwapHistoricalOrders.

    Args:
        list (List[TwapOrder]): List of TWAP orders.
        total (int): Total records.

    """

    list: list["TwapOrder"]
    total: int


class TwapOrder(BaseModel):
    """Model for a TWAP order.

    Args:
        symbol (str): Trading pair.
        main_order_id (str): TWAP order number.
        side (str): Buying and selling direction (SELL, BUY).
        position_side (str): LONG or SHORT.
        price_type (str): Price limit type (constant or percentage).
        price_variance (str): Price difference or slippage ratio.
        trigger_price (str): Trigger price.
        interval (int): Time interval for order placing (5-120s).
        amount_per_order (str): Quantity of a single order.
        total_amount (str): Total trading volume.
        order_status (str): Order status.
        executed_qty (str): Volume.
        duration (int): Execution time in seconds.
        max_duration (int): Maximum execution time in seconds.
        created_time (int): Order creation time in milliseconds.
        update_time (int): Order update time in milliseconds.

    """

    symbol: str
    main_order_id: str = Field(..., alias="mainOrderId")
    side: str
    position_side: str = Field(..., alias="positionSide")
    price_type: str = Field(..., alias="priceType")
    price_variance: str = Field(..., alias="priceVariance")
    trigger_price: str = Field(..., alias="triggerPrice")
    interval: int
    amount_per_order: str = Field(..., alias="amountPerOrder")
    total_amount: str = Field(..., alias="totalAmount")
    order_status: str = Field(..., alias="orderStatus")
    executed_qty: str = Field(..., alias="executedQty")
    duration: int
    max_duration: int = Field(..., alias="maxDuration")
    created_time: int = Field(..., alias="createdTime")
    update_time: int = Field(..., alias="updateTime")


class QueryTwapOrderDetailsResponse(BaseModel):
    """Model for the response of QueryTwapOrderDetails.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (TwapOrderDetails): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "TwapOrderDetails"


class CancelTwapOrderResponse(BaseModel):
    """Model for the response of CancelTwapOrder.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp in milliseconds.
        data (TwapOrderDetails): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "TwapOrderDetails"


class TwapOrderDetails(BaseModel):
    """Model for the response data of QueryTwapOrderDetails and CancelTwapOrder.

    Args:
        symbol (str): Trading pair.
        main_order_id (str): TWAP order number.
        side (str): Buying and selling direction (SELL, BUY).
        position_side (str): LONG or SHORT.
        price_type (str): Price limit type (constant or percentage).
        price_variance (str): Price difference or slippage ratio.
        trigger_price (str): Trigger price.
        interval (int): Time interval for order placing (5-120s).
        amount_per_order (str): Quantity of a single order.
        total_amount (str): Total trading volume.
        order_status (str): Order status.
        executed_qty (str): Volume.
        duration (int): Execution time in seconds.
        max_duration (int): Maximum execution time in seconds.
        created_time (int): Order creation time in milliseconds.
        update_time (int): Order update time in milliseconds.

    """

    symbol: str
    main_order_id: str = Field(..., alias="mainOrderId")
    side: str
    position_side: str = Field(..., alias="positionSide")
    price_type: str = Field(..., alias="priceType")
    price_variance: str = Field(..., alias="priceVariance")
    trigger_price: str = Field(..., alias="triggerPrice")
    interval: int
    amount_per_order: str = Field(..., alias="amountPerOrder")
    total_amount: str = Field(..., alias="totalAmount")
    order_status: str = Field(..., alias="orderStatus")
    executed_qty: str = Field(..., alias="executedQty")
    duration: int
    max_duration: int = Field(..., alias="maxDuration")
    created_time: int = Field(..., alias="createdTime")
    update_time: int = Field(..., alias="updateTime")


class SwitchMultiAssetsModeResponse(BaseModel):
    """Model for the response of SwitchMultiAssetsMode.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (SwitchMultiAssetsModeData): The response data.

    """

    code: int
    msg: str
    data: "SwitchMultiAssetsModeData"


class SwitchMultiAssetsModeData(BaseModel):
    """Model for the response data of SwitchMultiAssetsMode.

    Args:
        asset_mode (str): Multi-assets mode (singleAssetMode or multiAssetsMode).

    """

    asset_mode: str = Field(..., alias="assetMode")


class QueryMultiAssetsModeResponse(BaseModel):
    """Model for the response of QueryMultiAssetsMode.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (QueryMultiAssetsModeData): The response data.

    """

    code: int
    msg: str
    data: "QueryMultiAssetsModeData"


class QueryMultiAssetsModeData(BaseModel):
    """Model for the response data of QueryMultiAssetsMode.

    Args:
        asset_mode (str): Multi-assets mode, singleAssetMode or multiAssetsMode.

    """

    asset_mode: str = Field(..., alias="assetMode")


class QueryMultiAssetsRulesResponse(BaseModel):
    """Model for the response of QueryMultiAssetsRules.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[QueryMultiAssetsRulesData]): The response data.

    """

    code: int
    msg: str
    data: list["QueryMultiAssetsRulesData"]


class QueryMultiAssetsRulesData(BaseModel):
    """Model for the response data of QueryMultiAssetsRules.

    Args:
        margin_assets (str): Margin assets, such as BTC, ETH, etc.
        ltv (str): Loan-to-Value ratio, value conversion ratio used when calculating available margin.
        collateral_value_ratio (str): Collateral ratio, value conversion ratio used when calculating risk rate.
        max_transfer (str): Transfer limit, maximum amount that can be transferred in. Empty means no limit.
        index_price (str): Current latest USD index price for the asset.

    """

    margin_assets: str = Field(..., alias="marginAssets")
    ltv: str
    collateral_value_ratio: str = Field(..., alias="collateralValueRatio")
    max_transfer: str = Field(..., alias="maxTransfer")
    index_price: str = Field(..., alias="indexPrice")


class QueryMultiAssetsMarginResponse(BaseModel):
    """Model for the response of QueryMultiAssetsMargin.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[QueryMultiAssetsMarginData]): The response data.

    """

    code: int
    msg: str
    data: list["QueryMultiAssetsMarginData"]


class QueryMultiAssetsMarginData(BaseModel):
    """Model for the response data of QueryMultiAssetsMargin.

    Args:
        currency (str): Margin assets, such as BTC and ETH etc.
        total_amount (str): Total amount of margin assets.
        available_transfer (str): Current available amount for transfer out.
        latest_mortgage_amount (str): Latest collateral amount available.

    """

    currency: str
    total_amount: str = Field(..., alias="totalAmount")
    available_transfer: str = Field(..., alias="availableTransfer")
    latest_mortgage_amount: str = Field(..., alias="latestMortgageAmount")


class OneClickReversePositionResponse(BaseModel):
    """Model for the response of OneClickReversePosition.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        timestamp (int): Response timestamp.
        data (OneClickReversePositionData): The response data.

    """

    code: int
    msg: str
    timestamp: int
    data: "OneClickReversePositionData"


class OneClickReversePositionData(BaseModel):
    """Model for the response data of OneClickReversePosition.

    Args:
        type (str): Reverse type, Reverse: immediate reverse, TriggerReverse: planned reverse.
        position_id (str): Original position ID.
        new_position_id (str): New position ID.
        symbol (str): Trading pair, e.g.: BTC-USDT.
        position_side (str): Position side LONG/SHORT.
        isolated (bool): Whether in isolated mode, true: isolated mode, false: cross margin.
        position_amt (str): Position amount.
        available_amt (str): Available amount for closing.
        unrealized_profit (str): Unrealized profit and loss.
        realized_profit (str): Realized profit and loss.
        initial_margin (str): Initial margin.
        margin (str): Margin.
        liquidation_price (float): Liquidation price.
        avg_price (str): Average entry price.
        leverage (int): Leverage.
        position_value (str): Position value.
        mark_price (str): Mark price.
        risk_rate (str): Risk rate, position will be force-reduced or liquidated when risk rate reaches 100%.
        max_margin_reduction (str): Maximum reducible margin.
        pnl_ratio (str): Unrealized PNL ratio.
        update_time (int): Position update time in milliseconds.

    """

    type: str
    position_id: str = Field(..., alias="positionId")
    new_position_id: str = Field(..., alias="newPositionId")
    symbol: str
    position_side: str = Field(..., alias="positionSide")
    isolated: bool
    position_amt: str = Field(..., alias="positionAmt")
    available_amt: str = Field(..., alias="availableAmt")
    unrealized_profit: str = Field(..., alias="unrealizedProfit")
    realized_profit: str = Field(..., alias="realizedProfit")
    initial_margin: str = Field(..., alias="initialMargin")
    margin: str
    liquidation_price: float = Field(..., alias="liquidationPrice")
    avg_price: str = Field(..., alias="avgPrice")
    leverage: int
    position_value: str = Field(..., alias="positionValue")
    mark_price: str = Field(..., alias="markPrice")
    risk_rate: str = Field(..., alias="riskRate")
    max_margin_reduction: str = Field(..., alias="maxMarginReduction")
    pnl_ratio: str = Field(..., alias="pnlRatio")
    update_time: int = Field(..., alias="updateTime")


class HedgeModeAutoAddMarginResponse(BaseModel):
    """Model for the response of HedgeModeAutoAddMargin.

    Args:
        code (int): Error code, 0 means success, non-zero means failure.
        msg (str): Error message.
        amount (int): Amount of margin added, in USDT.
        type (int): Response type.

    """

    code: int
    msg: str
    amount: int
    type: int
