from typing import Optional

from pydantic import BaseModel, Field


class PositionItem(BaseModel):
    """Model for position data.

    Args:
        symbol (str): Trading pair.
        initial_margin (Optional[float]): Margin.
        leverage (Optional[float]): Leverage.
        unrealized_profit (Optional[float]): Position unrealized profit and loss.
        isolated (Optional[bool]): Whether it is isolated margin mode.
        entry_price (Optional[float]): Holding cost price.
        position_side (Optional[float]): Position direction, LONG and SHORT.
        position_amt (Optional[float]): Transaction data.
        current_price (Optional[float]): Current price. When there is no closing price, the current price will be returned.
        time (int): Opening time.

    """

    symbol: str = Field(..., description="Trading pair")
    initial_margin: Optional[float] = Field(
        None,
        description="Margin",
        alias="initialMargin",
    )
    leverage: Optional[float] = Field(None, description="Leverage")
    unrealized_profit: Optional[float] = Field(
        None,
        description="Position unrealized profit and loss",
        alias="unrealizedProfit",
    )
    isolated: Optional[bool] = Field(
        None,
        description="Whether it is isolated margin mode",
    )
    entry_price: Optional[float] = Field(
        None,
        description="Holding cost price",
        alias="entryPrice",
    )
    position_side: Optional[float] = Field(
        None,
        description="Position direction, LONG and SHORT",
        alias="positionSide",
    )
    position_amt: Optional[float] = Field(
        None,
        description="Transaction data",
        alias="positionAmt",
    )
    current_price: Optional[float] = Field(
        None,
        description="Current price. When there is no closing price, the current price will be returned",
        alias="currentPrice",
    )
    time: int = Field(..., description="Opening time")


class PositionsResponse(BaseModel):
    """Model for the response of Query Invited Users.

    Args:
    - `code` (int): Error code, 0 means successful response, others mean response failure.
    - `timestamp` (int): Response timestamp.
    - `data` (List[PositionItem]): Response data.

    """

    code: int = Field(..., description="Error code, 0 means success")
    timestamp: int = Field(..., description="Response timestamp")
    data: list[PositionItem] = Field(..., description="List of position items")


class HistoricalOrderItem(BaseModel):
    """Model for historical order item.

    Args:
    - `avg_price` (Optional[float]): Closing price.
    - `cum_quote` (Optional[float]): Transaction amount.
    - `executed_qty` (Optional[float]): Turnover.
    - `order_id` (Optional[int]): System order number.
    - `position_side` (str): Position direction, LONG and SHORT.
    - `status` (str): Order Status CLOSED.
    - `symbol` (str): Currency pair, the format is similar to: BTC-USDT.
    - `time` (int): Order time.
    - `update_time` (int): Update time.
    - `margin` (Optional[float]): Margin.
    - `leverage` (Optional[float]): Leverage.
    - `isolated` (Optional[bool]): Whether it is isolated margin mode.
    - `close_price` (Optional[float]): Closing price.
    - `position_id` (int): Position order number.

    """

    avg_price: Optional[float] = Field(
        None,
        description="Closing price",
        alias="avgPrice",
    )
    cum_quote: Optional[float] = Field(
        None,
        description="Transaction amount",
        alias="cumQuote",
    )
    executed_qty: Optional[float] = Field(
        None,
        description="Turnover",
        alias="executedQty",
    )
    order_id: Optional[int] = Field(
        None,
        description="System order number",
        alias="orderId",
    )
    position_side: str = Field(
        ...,
        description="Position direction, LONG and SHORT",
        alias="positionSide",
    )
    status: str = Field(..., description="Order Status CLOSED")
    symbol: str = Field(
        ...,
        description="Currency pair, the format is similar to: BTC-USDT",
    )
    time: int = Field(..., description="Order time")
    update_time: int = Field(..., description="Update time", alias="updateTime")
    margin: Optional[float] = Field(None, description="Margin")
    leverage: Optional[float] = Field(None, description="Leverage")
    isolated: Optional[bool] = Field(
        None,
        description="Whether it is isolated margin mode",
    )
    close_price: Optional[float] = Field(
        None,
        description="Closing price",
        alias="closePrice",
    )
    position_id: int = Field(
        ...,
        description="Position order number",
        alias="positionId",
    )


class HistoricalOrderResponse(BaseModel):
    """Model for the response of Historical Order.

    Args:
    - `code` (int): Error code, 0 means successful response, others mean response failure.
    - `timestamp` (int): Response timestamp.
    - `data` (List[HistoricalOrderItem]): Response data.

    """

    code: int = Field(..., description="Error code, 0 means success")
    timestamp: int = Field(..., description="Response timestamp")
    data: list[HistoricalOrderItem] = Field(
        ...,
        description="List of historical order items",
    )


class StandardContractBalanceItem(BaseModel):
    """Model for standard contract balance item.

    Args:
    - `asset` (str): Assets.
    - `balance` (str): Total balance.
    - `cross_wallet_balance` (str): Cross position balance.
    - `cross_un_pnl` (str): Unrealized profit and loss of cross positions.
    - `available_balance` (str): Order available balance.
    - `max_withdraw_amount` (str): Maximum transferable balance.
    - `margin_available` (Optional[bool]): Can it be used as a joint bond.
    - `update_time` (Optional[float]): Timestamp.

    """

    asset: str = Field(..., description="Assets")
    balance: str = Field(..., description="Total balance")
    cross_wallet_balance: str = Field(
        ...,
        description="Cross position balance",
        alias="crossWalletBalance",
    )
    cross_un_pnl: str = Field(
        ...,
        description="Unrealized profit and loss of cross positions",
        alias="crossUnPnl",
    )
    available_balance: str = Field(
        ...,
        description="Order available balance",
        alias="availableBalance",
    )
    max_withdraw_amount: str = Field(
        ...,
        description="Maximum transferable balance",
        alias="maxWithdrawAmount",
    )
    margin_available: Optional[bool] = Field(
        None,
        description="Can it be used as a joint bond",
        alias="marginAvailable",
    )
    update_time: Optional[float] = Field(
        None,
        description="Timestamp",
        alias="updateTime",
    )


class StandardContractBalanceResponse(BaseModel):
    """Model for the response of Historical Order.

    Args:
    - `code` (int): Error code, 0 means successful response, others mean response failure.
    - `timestamp` (int): Response timestamp.
    - `data` (List[StandardContractBalanceItem]): Response data.

    """

    code: int = Field(..., description="Error code, 0 means success")
    timestamp: int = Field(..., description="Response timestamp")
    data: list[StandardContractBalanceItem] = Field(..., description="List of balances")
