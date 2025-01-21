from typing import Union

from pydantic import BaseModel, Field


class SpotTradingSymbol(BaseModel):
    """Model for a single spot trading symbol.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        min_qty (float): Minimum order quantity.
        max_qty (float): Maximum order quantity.
        min_notional (float): Minimum notional value.
        max_notional (float): Maximum notional value.
        status (int): Symbol status (1=active, 0=inactive).
        tick_size (float): Tick size.
        step_size (float): Step size.

    """

    symbol: str = Field(..., description="Trading pair, e.g., BTC-USDT")
    min_qty: float = Field(..., description="Minimum order quantity", alias="minQty")
    max_qty: float = Field(..., description="Maximum order quantity", alias="maxQty")
    min_notional: float = Field(
        ...,
        description="Minimum notional value",
        alias="minNotional",
    )
    max_notional: float = Field(
        ...,
        description="Maximum notional value",
        alias="maxNotional",
    )
    status: int = Field(..., description="Symbol status (1=active, 0=inactive)")
    tick_size: float = Field(..., description="Tick size", alias="tickSize")
    step_size: float = Field(..., description="Step size", alias="stepSize")


class SpotTradingSymbolsResponseData(BaseModel):
    """Model for the data field in SpotTradingSymbolsResponse.

    Args:
        symbols (List[SpotTradingSymbol]): List of spot trading symbols.

    """

    symbols: list[SpotTradingSymbol] = Field(
        ...,
        description="List of spot trading symbols",
    )


class SpotTradingSymbolsResponse(BaseModel):
    """Model for the response of Spot Trading Symbols.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        msg (str): Error Details Description.
        debug_msg (str): Debug message.
        data (SpotTradingSymbolsResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    msg: str = Field(..., description="Error Details Description")
    debug_msg: str = Field(..., description="Debug message", alias="debugMsg")
    data: SpotTradingSymbolsResponseData = Field(..., description="Response data")


class RecentTrade(BaseModel):
    """Model for a single recent trade.

    Args:
        id (int): Transaction ID.
        price (float): Price.
        qty (float): Quantity.
        time (int): Time of the trade.
        buyer_maker (bool): Whether the buyer is the maker.

    """

    id: int = Field(..., description="Transaction ID")
    price: float = Field(..., description="Price")
    qty: float = Field(..., description="Quantity")
    time: int = Field(..., description="Time of the trade")
    buyer_maker: bool = Field(
        ...,
        description="Whether the buyer is the maker",
        alias="buyerMaker",
    )


class RecentTradesListResponse(BaseModel):
    """Model for the response of Recent Trades List.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[RecentTrade]): List of recent trades.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[RecentTrade] = Field(..., description="List of recent trades")


class OrderBookResponseData(BaseModel):
    """Model for the data field in OrderBookResponse.

    Args:
        bids (List[List[str]]): List of bids, each bid is a list of [price, quantity].
        asks (List[List[str]]): List of asks, each ask is a list of [price, quantity].
        ts (int): Timestamp of the order book.

    """

    bids: list[list[str]] = Field(
        ...,
        description="List of bids, each bid is a list of [price, quantity]",
    )
    asks: list[list[str]] = Field(
        ...,
        description="List of asks, each ask is a list of [price, quantity]",
    )
    ts: int = Field(..., description="Timestamp of the order book")


class OrderBookResponse(BaseModel):
    """Model for the response of Order Book.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (OrderBookResponseData): Order book data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: OrderBookResponseData = Field(..., description="Order book data")


class KlineDataResponse(BaseModel):
    """Model for the response of Kline/Candlestick Data.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[List[Union[int, float]]]): List of klines, each kline is a list of [timestamp, open, high, low, close, volume, close_time, quote_asset_volume].

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[list[Union[int, float]]] = Field(
        ...,
        description="List of klines, each kline is a list of [timestamp, open, high, low, close, volume, close_time, quote_asset_volume]",
    )


class Ticker24hr(BaseModel):
    """Model for 24hr ticker price change statistics.

    Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        open_price (str): Opening price in the last 24 hours.
        high_price (str): The highest price in the last 24 hours.
        low_price (str): The lowest price in the last 24 hours.
        last_price (str): Latest price.
        volume (str): Total trading volume (base asset).
        quote_volume (str): Total quote volume (quote asset).
        open_time (int): The start time of the ticker interval.
        close_time (int): End time of the ticker interval.
        bid_price (float): Bid price.
        bid_qty (float): Bid quantity.
        ask_price (float): Ask price.
        ask_qty (float): Ask quantity.
        price_change_percent (str): Price change percentage.

    """

    symbol: str = Field(..., description="Trading pair, e.g., BTC-USDT")
    open_price: str = Field(
        ...,
        description="Opening price in the last 24 hours",
        alias="openPrice",
    )
    high_price: str = Field(
        ...,
        description="The highest price in the last 24 hours",
        alias="highPrice",
    )
    low_price: str = Field(
        ...,
        description="The lowest price in the last 24 hours",
        alias="lowPrice",
    )
    last_price: str = Field(..., description="Latest price", alias="lastPrice")
    volume: str = Field(..., description="Total trading volume (base asset)")
    quote_volume: str = Field(
        ...,
        description="Total quote volume (quote asset)",
        alias="quoteVolume",
    )
    open_time: int = Field(
        ...,
        description="The start time of the ticker interval",
        alias="openTime",
    )
    close_time: int = Field(
        ...,
        description="End time of the ticker interval",
        alias="closeTime",
    )
    bid_price: float = Field(..., description="Bid price", alias="bidPrice")
    bid_qty: float = Field(..., description="Bid quantity", alias="bidQty")
    ask_price: float = Field(..., description="Ask price", alias="askPrice")
    ask_qty: float = Field(..., description="Ask quantity", alias="askQty")
    price_change_percent: str = Field(
        ...,
        description="Price change percentage",
        alias="priceChangePercent",
    )


class Ticker24hrResponse(BaseModel):
    """Model for the response of 24hr ticker price change statistics.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[Ticker24hr]): List of ticker data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[Ticker24hr] = Field(..., description="List of ticker data")


class OrderBookAggregationResponseData(BaseModel):
    """Model for the data field in OrderBookAggregationResponse.

    Args:
        bids (List[List[str]]): Buy depth, where the first element is the price and the second is the quantity.
        asks (List[List[str]]): Sell depth, where the first element is the price and the second is the quantity.
        ts (int): Timestamp.

    """

    bids: list[list[str]] = Field(
        ...,
        description="Buy depth, where the first element is the price and the second is the quantity",
    )
    asks: list[list[str]] = Field(
        ...,
        description="Sell depth, where the first element is the price and the second is the quantity",
    )
    ts: int = Field(..., description="Timestamp")


class OrderBookAggregationResponse(BaseModel):
    """Model for the response of Order Book Aggregation.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (OrderBookAggregationResponseData): Order book data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: OrderBookAggregationResponseData = Field(..., description="Order book data")


class TradeItem(BaseModel):
    """Model for a trade item.

    Args:
        timestamp (int): Trade timestamp in milliseconds.
        trade_id (str): Trade ID.
        price (str): Trade price.
        amount (str): Trade amount (empty in this case).
        type (int): Trade type (1 for buy, 2 for sell, etc.).
        volume (str): Trade volume.

    """

    timestamp: int
    trade_id: str = Field(..., alias="tradeId")
    price: str
    amount: str
    type: int
    volume: str


class SymbolPriceTickerResponseData(BaseModel):
    """Model for the data field in SymbolPriceTickerResponse.

    Args:
        symbol (str): Trading pair, e.g., BTC_USDT.
        trades (List[Trade]): List of trades.

    """

    symbol: str = Field(..., description="Trading pair, e.g., BTC_USDT")
    trades: list["TradeItem"] = Field(..., description="List of trades")


class SymbolPriceTickerResponse(BaseModel):
    """Model for the response of Symbol Price Ticker.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[SymbolPriceTickerResponseData]): List of symbol price ticker data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[SymbolPriceTickerResponseData] = Field(
        ...,
        description="List of symbol price ticker data",
    )


class SymbolOrderBookTickerResponseData(BaseModel):
    """Model for the data field in SymbolOrderBookTickerResponse.

    Args:
        event_type (str): Data type.
        time (int): Timestamp.
        symbol (str): Trading pair, e.g., BTC-USDT.
        bid_price (str): Best bid price.
        bid_volume (str): Best bid volume.
        ask_price (str): Best ask price.
        ask_volume (str): Best ask volume.

    """

    event_type: str = Field(..., description="Data type", alias="eventType")
    time: int = Field(..., description="Timestamp")
    symbol: str = Field(..., description="Trading pair, e.g., BTC-USDT")
    bid_price: str = Field(..., description="Best bid price", alias="bidPrice")
    bid_volume: str = Field(..., description="Best bid volume", alias="bidVolume")
    ask_price: str = Field(..., description="Best ask price", alias="askPrice")
    ask_volume: str = Field(..., description="Best ask volume", alias="askVolume")


class SpotSymbolOrderBookTickerResponse(BaseModel):
    """Model for the response of Symbol Order Book Ticker.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[SymbolOrderBookTickerResponseData]): List of order book ticker data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[SymbolOrderBookTickerResponseData] = Field(
        ...,
        description="List of order book ticker data",
    )


class HistoricalKlineResponse(BaseModel):
    """Model for the response of Historical K-line.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[List[Union[int, float]]]): List of klines, each kline is a list of [timestamp, open, high, low, close, volume, close_time, quote_asset_volume].

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[list[Union[int, float]]] = Field(
        ...,
        description="List of klines, each kline is a list of [timestamp, open, high, low, close, volume, close_time, quote_asset_volume]",
    )


class OldTrade(BaseModel):
    """Model for a single old trade.

    Args:
        tid (str): Trade ID.
        t (int): Trade time.
        ms (int): Milliseconds.
        s (str): Trading pair, e.g., BTC-USDT.
        p (float): Price.
        v (float): Volume.

    """

    tid: str = Field(..., description="Trade ID")
    t: int = Field(..., description="Trade time")
    ms: int = Field(..., description="Milliseconds")
    s: str = Field(..., description="Trading pair, e.g., BTC-USDT")
    p: float = Field(..., description="Price")
    v: float = Field(..., description="Volume")


class OldTradeLookupResponse(BaseModel):
    """Model for the response of Old Trade Lookup.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (List[OldTrade]): List of old trades.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: list[OldTrade] = Field(..., description="List of old trades")
