from enum import Enum

from pydantic import BaseModel, Field


class ContractStatus(Enum):
    """Enum for contract status.

    Values:
        ONLINE: 1
        FORBIDDEN_TO_OPEN: 25
        PRE_ONLINE: 5
        OFFLINE: 0
    """

    ONLINE = 1
    FORBIDDEN_TO_OPEN = 25
    PRE_ONLINE = 5
    OFFLINE = 0


class ApiState(Enum):
    """Enum for API state.

    Values:
        TRUE: "true"
        FALSE: "false"
    """

    TRUE = "true"
    FALSE = "false"


class BrokerState(Enum):
    """Enum for broker state.

    Values:
        TRUE: "true"
        FALSE: "false"
    """

    TRUE = "true"
    FALSE = "false"


class UsdtMPerpFuturesSymbolsResponse(BaseModel):
    """Model for the response of USDT-M Perp Futures symbols.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (List[Contract]): Array of contracts

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: list["Contract"] = Field(..., description="Array of contracts")


class Contract(BaseModel):
    """Model for a contract in USDT-M Perp Futures symbols.

    Args:
        contract_id (str): Contract ID
        symbol (str): Trading pair, for example: BTC-USDT
        quantity_precision (int): Transaction quantity precision
        price_precision (int): Price precision
        taker_fee_rate (float): Take transaction fee
        maker_fee_rate (float): Make transaction fee
        trade_min_quantity (float): The minimum trading unit(COIN)
        trade_min_usdt (float): The minimum trading unit(USDT)
        currency (str): Settlement and margin currency asset
        asset (str): Contract trading asset
        status (ContractStatus): Contract status (1 online, 25 forbidden to open positions, 5 pre-online, 0 offline)
        api_state_open (ApiState): Whether the API can open a position
        api_state_close (ApiState): Whether API can close positions
        ensure_trigger (bool): Whether to support guaranteed stop loss
        trigger_fee_rate (str): The fee rate for guaranteed stop loss
        broker_state (BrokerState): Whether to prohibit broker user transactions, true: prohibited
        launch_time (int): Shelf time; The status of the pair is pre-online before the listing time, and the status of the pair changes to online after the listing time
        maintain_time (int): The start time of the prohibition of opening a position, after the time is up, the currency pair is in a state of prohibition from opening a position, and can only close the position
        off_time (int): Down line time, after the time is up, the currency pair is in the offline state and trading is prohibited

    """

    contract_id: str = Field(..., description="Contract ID", alias="contractId")
    symbol: str = Field(..., description="Trading pair, for example: BTC-USDT")
    quantity_precision: int = Field(
        ...,
        description="Transaction quantity precision",
        alias="quantityPrecision",
    )
    price_precision: int = Field(
        ...,
        description="Price precision",
        alias="pricePrecision",
    )
    taker_fee_rate: float = Field(
        ...,
        description="Take transaction fee",
        alias="takerFeeRate",
    )
    maker_fee_rate: float = Field(
        ...,
        description="Make transaction fee",
        alias="makerFeeRate",
    )
    trade_min_quantity: float = Field(
        ...,
        description="The minimum trading unit(COIN)",
        alias="tradeMinQuantity",
    )
    trade_min_usdt: float = Field(
        ...,
        description="The minimum trading unit(USDT)",
        alias="tradeMinUSDT",
    )
    currency: str = Field(..., description="Settlement and margin currency asset")
    asset: str = Field(..., description="Contract trading asset")
    status: ContractStatus = Field(
        ...,
        description="1 online, 25 forbidden to open positions, 5 pre-online, 0 offline",
    )
    api_state_open: ApiState = Field(
        ...,
        description="Whether the API can open a position",
        alias="apiStateOpen",
    )
    api_state_close: ApiState = Field(
        ...,
        description="Whether API can close positions",
        alias="apiStateClose",
    )
    ensure_trigger: bool = Field(
        ...,
        description="Whether to support guaranteed stop loss",
        alias="ensureTrigger",
    )
    trigger_fee_rate: str = Field(
        ...,
        description="The fee rate for guaranteed stop loss",
        alias="triggerFeeRate",
    )
    broker_state: BrokerState = Field(
        ...,
        description="Whether to prohibit broker user transactions, true: prohibited",
        alias="brokerState",
    )
    launch_time: int = Field(
        ...,
        description="Shelf time; The status of the pair is pre-online before the listing time, and the status of the pair changes to online after the listing time",
        alias="launchTime",
    )
    maintain_time: int = Field(
        ...,
        description="The start time of the prohibition of opening a position, after the time is up, the currency pair is in a state of prohibition from opening a position, and can only close the position",
        alias="maintainTime",
    )
    off_time: int = Field(
        ...,
        description="Down line time, after the time is up, the currency pair is in the offline state and trading is prohibited",
        alias="offTime",
    )


class SwapOrderBookResponse(BaseModel):
    """Model for the response of Order Book.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (OrderBookData): Order book data

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: "OrderBookData" = Field(..., description="Order book data")


class OrderBookData(BaseModel):
    """Model for the order book data.

    Args:
        T (int): System time, unit: millisecond
        bids (List[List[str]]): Buyer depth. first element price, second element quantity
        asks (List[List[str]]): Depth of asks. first element price, second element quantity
        bids_coin (List[List[str]]): Buyer depth. first element price, second element quantity(coin)
        asks_coin (List[List[str]]): Depth of asks. first element price, second element quantity(coin)

    """

    T: int = Field(..., description="System time, unit: millisecond")
    bids: list[list[str]] = Field(
        ...,
        description="Buyer depth. first element price, second element quantity",
    )
    asks: list[list[str]] = Field(
        ...,
        description="Depth of asks. first element price, second element quantity",
    )
    bids_coin: list[list[str]] = Field(
        ...,
        description="Buyer depth. first element price, second element quantity(coin)",
        alias="bidsCoin",
    )
    asks_coin: list[list[str]] = Field(
        ...,
        description="Depth of asks. first element price, second element quantity(coin)",
        alias="asksCoin",
    )


class SwapRecentTradesListResponse(BaseModel):
    """Model for the response of Recent Trades List.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (List[Trade]): Array of trades

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: list["Trade"] = Field(..., description="Array of trades")


class Trade(BaseModel):
    """Model for a trade in Recent Trades List.

    Args:
        time (int): Transaction time
        is_buyer_maker (bool): Whether the buyer is the maker of the order (true / false)
        price (str): Transaction price
        qty (str): Transaction quantity
        quote_qty (str): Turnover

    """

    time: int = Field(..., description="Transaction time")
    is_buyer_maker: bool = Field(
        ...,
        description="Whether the buyer is the maker of the order (true / false)",
        alias="isBuyerMaker",
    )
    price: str = Field(..., description="Transaction price")
    qty: str = Field(..., description="Transaction quantity")
    quote_qty: str = Field(..., description="Turnover", alias="quoteQty")


class MarkPriceAndFundingRateResponse(BaseModel):
    """Model for the response of Mark Price and Funding Rate.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (MarkPriceAndFundingRateData): The response data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: "MarkPriceAndFundingRateData" = Field(..., description="The response data.")


class MarkPriceAndFundingRateData(BaseModel):
    """Model for the data of Mark Price and Funding Rate.

    Args:
        symbol (str): Trading pair, for example: BTC-USDT
        mark_price (str): Current mark price
        index_price (str): Index price
        last_funding_rate (str): Last updated funding rate
        next_funding_time (int): The remaining time for the next settlement, in milliseconds

    """

    symbol: str = Field(..., description="Trading pair, for example: BTC-USDT")
    mark_price: str = Field(..., description="Current mark price", alias="markPrice")
    index_price: str = Field(..., description="Index price", alias="indexPrice")
    last_funding_rate: str = Field(
        ...,
        description="Last updated funding rate",
        alias="lastFundingRate",
    )
    next_funding_time: int = Field(
        ...,
        description="The remaining time for the next settlement, in milliseconds",
        alias="nextFundingTime",
    )


class GetFundingRateHistoryResponse(BaseModel):
    """Model for the response of Get Funding Rate History.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (List[FundingRateHistory]): Array of funding rate history.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: list["FundingRateHistory"] = Field(
        ...,
        description="Array of funding rate history.",
    )


class FundingRateHistory(BaseModel):
    """Model for the data of Funding Rate History.

    Args:
        symbol (str): Trading pair, for example: BTC-USDT
        funding_rate (str): Funding rate
        funding_time (int): Funding time: milliseconds

    """

    symbol: str = Field(..., description="Trading pair, for example: BTC-USDT")
    funding_rate: str = Field(..., description="Funding rate", alias="fundingRate")
    funding_time: int = Field(
        ...,
        description="Funding time: milliseconds",
        alias="fundingTime",
    )


class KlineCandlestickDataResponse(BaseModel):
    """Model for the response of Kline/Candlestick Data.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (List[KlineCandlestick]): Array of kline/candlestick data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: list["KlineCandlestick"] = Field(
        ...,
        description="Array of kline/candlestick data.",
    )


class KlineCandlestick(BaseModel):
    """Model for the data of Kline/Candlestick.

    Args:
        open (float): Opening Price
        close (float): Closing Price
        high (float): High Price
        low (float): Low Price
        volume (float): Transaction volume
        time (int): K-line time stamp, unit milliseconds

    """

    open: float = Field(..., description="Opening Price")
    close: float = Field(..., description="Closing Price")
    high: float = Field(..., description="High Price")
    low: float = Field(..., description="Low Price")
    volume: float = Field(..., description="Transaction volume")
    time: int = Field(..., description="K-line time stamp, unit milliseconds")


class OpenInterestStatisticsResponse(BaseModel):
    """Model for the response of Open Interest Statistics.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (OpenInterestStatisticsData): The response data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: "OpenInterestStatisticsData" = Field(..., description="The response data.")


class OpenInterestStatisticsData(BaseModel):
    """Model for the data of Open Interest Statistics.

    Args:
        open_interest (str): Position Amount
        symbol (str): Contract name
        time (int): Matching engine time

    """

    open_interest: str = Field(..., description="Position Amount", alias="openInterest")
    symbol: str = Field(..., description="Contract name")
    time: int = Field(..., description="Matching engine time")


class TickerPriceChangeStatisticsResponse(BaseModel):
    """Model for the response of 24hr Ticker Price Change Statistics.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (TickerPriceChangeStatisticsData): The response data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: "TickerPriceChangeStatisticsData" = Field(
        ...,
        description="The response data.",
    )


class TickerPriceChangeStatisticsData(BaseModel):
    """Model for the data of 24hr Ticker Price Change Statistics.

    Args:
        symbol (str): Trading pair, for example: BTC-USDT
        price_change (str): 24 hour price change
        price_change_percent (str): Price change percentage
        last_price (str): Latest transaction price
        last_qty (str): Latest transaction amount
        high_price (str): 24-hour highest price
        low_price (str): 24 hours lowest price
        volume (str): 24-hour volume
        quote_volume (str): 24-hour turnover, the unit is USDT
        open_price (str): First price within 24 hours
        open_time (int): The time when the first transaction occurred within 24 hours
        close_time (int): The time when the last transaction occurred within 24 hours
        bid_price (float): Bid price
        bid_qty (float): Bid quantity
        ask_price (float): Ask price
        ask_qty (float): Ask quantity

    """

    symbol: str = Field(..., description="Trading pair, for example: BTC-USDT")
    price_change: str = Field(
        ...,
        description="24 hour price change",
        alias="priceChange",
    )
    price_change_percent: str = Field(
        ...,
        description="Price change percentage",
        alias="priceChangePercent",
    )
    last_price: str = Field(
        ...,
        description="Latest transaction price",
        alias="lastPrice",
    )
    last_qty: str = Field(..., description="Latest transaction amount", alias="lastQty")
    high_price: str = Field(..., description="24-hour highest price", alias="highPrice")
    low_price: str = Field(..., description="24 hours lowest price", alias="lowPrice")
    volume: str = Field(..., description="24-hour volume")
    quote_volume: str = Field(
        ...,
        description="24-hour turnover, the unit is USDT",
        alias="quoteVolume",
    )
    open_price: str = Field(
        ...,
        description="First price within 24 hours",
        alias="openPrice",
    )
    open_time: int = Field(
        ...,
        description="The time when the first transaction occurred within 24 hours",
        alias="openTime",
    )
    close_time: int = Field(
        ...,
        description="The time when the last transaction occurred within 24 hours",
        alias="closeTime",
    )
    bid_price: float = Field(..., description="Bid price", alias="bidPrice")
    bid_qty: float = Field(..., description="Bid quantity", alias="bidQty")
    ask_price: float = Field(..., description="Ask price", alias="askPrice")
    ask_qty: float = Field(..., description="Ask quantity", alias="askQty")


class SwapQueryHistoricalTransactionOrdersResponse(BaseModel):
    """Model for the response of Query historical transaction orders.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (List[HistoricalTransactionOrder]): Array of historical transaction orders.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: list["HistoricalTransactionOrder"] = Field(
        ...,
        description="Array of historical transaction orders.",
    )


class HistoricalTransactionOrder(BaseModel):
    """Model for the data of Historical Transaction Order.

    Args:
        time (int): Transaction time
        is_buyer_maker (bool): Whether the buyer is the maker of the order (true / false)
        price (str): Transaction price
        qty (str): Transaction quantity
        quote_qty (str): Turnover
        id (str): Transaction ID

    """

    time: int = Field(..., description="Transaction time")
    is_buyer_maker: bool = Field(
        ...,
        description="Whether the buyer is the maker of the order (true / false)",
        alias="isBuyerMaker",
    )
    price: str = Field(..., description="Transaction price")
    qty: str = Field(..., description="Transaction quantity")
    quote_qty: str = Field(..., description="Turnover", alias="quoteQty")
    id: str = Field(..., description="Transaction ID")


class SymbolOrderBookTickerResponse(BaseModel):
    """Model for the response of Symbol Order Book Ticker.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (SymbolOrderBookTickerData): The response data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: "SymbolOrderBookTickerData" = Field(..., description="The response data.")


class SymbolOrderBookTickerData(BaseModel):
    """Model for the data of Symbol Order Book Ticker.

    Args:
        symbol (str): Trading pair, for example: BTC-USDT
        bid_price (float): Optimal purchase price
        bid_qty (float): Order quantity
        ask_price (float): Best selling price
        ask_qty (float): Order quantity

    """

    symbol: str = Field(..., description="Trading pair, for example: BTC-USDT")
    bid_price: float = Field(
        ...,
        description="Optimal purchase price",
        alias="bidPrice",
    )
    bid_qty: float = Field(..., description="Order quantity", alias="bidQty")
    ask_price: float = Field(..., description="Best selling price", alias="askPrice")
    ask_qty: float = Field(..., description="Order quantity", alias="askQty")


class MarkPriceKlineCandlestickDataResponse(BaseModel):
    """Model for the response of Mark Price Kline/Candlestick Data.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (List[MarkPriceKlineCandlestick]): Array of mark price kline/candlestick data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: list["MarkPriceKlineCandlestick"] = Field(
        ...,
        description="Array of mark price kline/candlestick data.",
    )


class MarkPriceKlineCandlestick(BaseModel):
    """Model for the data of Mark Price Kline/Candlestick.

    Args:
        open (float): Opening Price
        close (float): Closing Price
        high (float): High Price
        low (float): Low Price
        volume (float): Transaction volume
        open_time (int): K-line open time stamp, unit milliseconds
        close_time (int): K-line close time stamp, unit milliseconds

    """

    open: float = Field(..., description="Opening Price")
    close: float = Field(..., description="Closing Price")
    high: float = Field(..., description="High Price")
    low: float = Field(..., description="Low Price")
    volume: float = Field(..., description="Transaction volume")
    open_time: int = Field(
        ...,
        description="K-line open time stamp, unit milliseconds",
        alias="openTime",
    )
    close_time: int = Field(
        ...,
        description="K-line close time stamp, unit milliseconds",
        alias="closeTime",
    )


class SwapSymbolPriceTickerResponse(BaseModel):
    """Model for the response of Symbol Price Ticker.

    Args:
        code (int): error code, 0 means successfully response, others means response failure
        msg (str): Error Details Description
        data (SymbolPriceTickerData): The response data.

    """

    code: int = Field(
        ...,
        description="error code, 0 means successfully response, others means response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    data: "SwapSymbolPriceTickerData" = Field(..., description="The response data.")


class SwapSymbolPriceTickerData(BaseModel):
    """Model for the data of Symbol Price Ticker.

    Args:
        symbol (str): Trading pair, for example: BTC-USDT
        price (str): Price
        time (int): Matching engine time

    """

    symbol: str = Field(..., description="Trading pair, for example: BTC-USDT")
    price: str = Field(..., description="Price")
    time: int = Field(..., description="Matching engine time")
