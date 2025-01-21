from pydantic import BaseModel, Field


class QueryAccountDataResponse(BaseModel):
    """Model for the response of QueryAccountData.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[AccountData]): The response data.

    """

    code: int
    msg: str
    data: list["AccountData"]


class AccountData(BaseModel):
    """Model for account data.

    Args:
        user_id (str): User ID.
        asset (str): Asset name, e.g., USDT.
        balance (str): Asset balance.
        equity (str): Net asset value.
        unrealized_profit (str): Unrealized profit and loss.
        realised_profit (str): Realized profit and loss.
        available_margin (str): Available margin.
        used_margin (str): Used margin.
        freezed_margin (str): Frozen margin.

    """

    user_id: str = Field(..., alias="userId")
    asset: str
    balance: str
    equity: str
    unrealized_profit: str = Field(..., alias="unrealizedProfit")
    realised_profit: str = Field(..., alias="realisedProfit")
    available_margin: str = Field(..., alias="availableMargin")
    used_margin: str = Field(..., alias="usedMargin")
    freezed_margin: str = Field(..., alias="freezedMargin")


class QueryPositionDataResponse(BaseModel):
    """Model for the response of QueryPositionData.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[PositionData]): The response data.

    """

    code: int
    msg: str
    data: list["PositionData"]


class PositionData(BaseModel):
    """Model for position data.

    Args:
        position_id (str): Position ID.
        symbol (str): Trading pair, e.g., BNB-USDT.
        currency (str): Currency, e.g., USDT.
        position_amt (str): Position amount.
        available_amt (str): Available amount.
        position_side (str): Position direction (LONG/SHORT).
        isolated (bool): Whether it is isolated margin mode.
        avg_price (str): Average opening price.
        initial_margin (str): Initial margin.
        leverage (int): Leverage.
        unrealized_profit (str): Unrealized profit and loss.
        realised_profit (str): Realized profit and loss.
        liquidation_price (float): Liquidation price.

    """

    position_id: str = Field(..., alias="positionId")
    symbol: str
    currency: str
    position_amt: str = Field(..., alias="positionAmt")
    available_amt: str = Field(..., alias="availableAmt")
    position_side: str = Field(..., alias="positionSide")
    isolated: bool
    avg_price: str = Field(..., alias="avgPrice")
    initial_margin: str = Field(..., alias="initialMargin")
    leverage: int
    unrealized_profit: str = Field(..., alias="unrealizedProfit")
    realised_profit: str = Field(..., alias="realisedProfit")
    liquidation_price: float = Field(..., alias="liquidationPrice")


class GetAccountProfitAndLossFundFlowResponse(BaseModel):
    """Model for the response of GetAccountProfitAndLossFundFlow.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (List[FundFlowData]): The response data.

    """

    code: int
    msg: str
    data: list["FundFlowData"]


class FundFlowData(BaseModel):
    """Model for fund flow data.

    Args:
        symbol (str): Trading pair, e.g., LDO-USDT.
        income_type (str): Income type, e.g., FUNDING_FEE.
        income (str): The amount of capital flow, positive numbers represent inflows, negative numbers represent outflows.
        asset (str): Asset content.
        info (str): Remarks, depending on the type of stream.
        time (int): Time, unit: millisecond.
        tran_id (str): Transfer ID.
        trade_id (str): The original transaction ID that caused the transaction.

    """

    symbol: str
    income_type: str = Field(..., alias="incomeType")
    income: str
    asset: str
    info: str
    time: int
    tran_id: str = Field(..., alias="tranId")
    trade_id: str = Field(..., alias="tradeId")


class SwapQueryTradingCommissionRateResponse(BaseModel):
    """Model for the response of QueryTradingCommissionRate.

    Args:
        code (int): Error code, 0 means successfully response, others means response failure.
        msg (str): Error details description.
        data (CommissionData): The response data.

    """

    code: int
    msg: str
    data: "CommissionData"


class CommissionData(BaseModel):
    """Model for commission data.

    Args:
        commission (CommissionDetails): Commission details.

    """

    commission: "CommissionDetails"


class CommissionDetails(BaseModel):
    """Model for commission details.

    Args:
        taker_commission_rate (float): Taker fee rate.
        maker_commission_rate (float): Maker fee rate.

    """

    taker_commission_rate: float = Field(..., alias="takerCommissionRate")
    maker_commission_rate: float = Field(..., alias="makerCommissionRate")
