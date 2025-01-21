from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.swap.market import (
    GetFundingRateHistoryResponse,
    KlineCandlestickDataResponse,
    MarkPriceAndFundingRateResponse,
    MarkPriceKlineCandlestickDataResponse,
    OpenInterestStatisticsResponse,
    SwapOrderBookResponse,
    SwapQueryHistoricalTransactionOrdersResponse,
    SwapRecentTradesListResponse,
    SwapSymbolPriceTickerResponse,
    SymbolOrderBookTickerResponse,
    TickerPriceChangeStatisticsResponse,
    UsdtMPerpFuturesSymbolsResponse,
)

if TYPE_CHECKING:
    from bingx_py.client import BingXHttpClient


class MarketAPI:
    """API for managing market on BingX."""

    def __init__(self, client: "BingXHttpClient") -> None:
        """Initialize the MarketAPI.

        Args:
            client (BingXHttpClient): The HTTP client used to interact with the BingX API.

        Returns:
            None

        """
        self.client = client

    def get_symbols(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> UsdtMPerpFuturesSymbolsResponse:
        """USDT-M Perp Futures symbols.

        Args:
            symbol (Optional[str]): Trading pair, for example: BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            UsdtMPerpFuturesSymbolsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/contracts", params=params),
            UsdtMPerpFuturesSymbolsResponse,
        )

    def get_order_book(
        self,
        symbol: str,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> SwapOrderBookResponse:
        """Order Book.

        Args:
            symbol (str): Trading pair, for example: BTC-USDT, please use capital letters.
            limit (Optional[int]): Default 20, optional value:[5, 10, 20, 50, 100, 500, 1000]. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            SwapOrderBookResponse: The response data.

        """
        params: dict[str, Any] = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/depth", params=params),
            SwapOrderBookResponse,
        )

    def get_recent_trades_list(
        self,
        symbol: str,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> SwapRecentTradesListResponse:
        """Recent Trades List.

        Args:
            symbol (str): There must be a hyphen/ "-" in the trading pair symbol. eg: BTC-USDT.
            limit (Optional[int]): Default: 500, maximum 1000. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            SwapRecentTradesListResponse: The response data.

        """
        params: dict[str, Any] = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/trades", params=params),
            SwapRecentTradesListResponse,
        )

    def mark_price_and_funding_rate(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> MarkPriceAndFundingRateResponse:
        """Mark Price and Funding Rate.

        Args:
            symbol (Optional[str]): Trading pair, for example: BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            MarkPriceAndFundingRateResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/premiumIndex", params=params),
            MarkPriceAndFundingRateResponse,
        )

    def get_funding_rate_history(
        self,
        symbol: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> GetFundingRateHistoryResponse:
        """Get Funding Rate History.

        Args:
            symbol (Optional[str]): Trading pair, for example: BTC-USDT. Defaults to None.
            start_time (Optional[int]): Start time, unit: millisecond. Defaults to None.
            end_time (Optional[int]): End time, unit: millisecond. Defaults to None.
            limit (Optional[int]): Default: 100, maximum: 1000. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            GetFundingRateHistoryResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/fundingRate", params=params),
            GetFundingRateHistoryResponse,
        )

    def kline_candlestick_data(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> KlineCandlestickDataResponse:
        """Kline/Candlestick Data.

        Args:
            symbol (str): Trading pair, for example: BTC-USDT.
            interval (str): Time interval, refer to field description.
            start_time (Optional[int]): Start time, unit: millisecond. Defaults to None.
            end_time (Optional[int]): End time, unit: millisecond. Defaults to None.
            limit (Optional[int]): Default: 500, maximum: 1440. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            KlineCandlestickDataResponse: The response data.

        """
        params: dict[str, Any] = {"symbol": symbol, "interval": interval}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v3/quote/klines", params=params),
            KlineCandlestickDataResponse,
        )

    def open_interest_statistics(
        self,
        symbol: str,
        recv_window: Optional[int] = None,
    ) -> OpenInterestStatisticsResponse:
        """Open Interest Statistics.

        Args:
            symbol (str): Trading pair, for example: BTC-USDT.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            OpenInterestStatisticsResponse: The response data.

        """
        params: dict[str, Any] = {"symbol": symbol}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/openInterest", params=params),
            OpenInterestStatisticsResponse,
        )

    def ticker_price_change_statistics(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> TickerPriceChangeStatisticsResponse:
        """24hr Ticker Price Change Statistics.

        Args:
            symbol (Optional[str]): Trading pair, for example: BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            TickerPriceChangeStatisticsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/ticker", params=params),
            TickerPriceChangeStatisticsResponse,
        )

    def get_market_historical_orders(
        self,
        from_id: Optional[int] = None,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> SwapQueryHistoricalTransactionOrdersResponse:
        """Query historical transaction orders.

        Args:
            from_id (Optional[int]): From which transaction ID to start returning. By default, it returns the most recent transaction records. Defaults to None.
            symbol (Optional[str]): Trading pair, for example: BTC-USDT. Defaults to None.
            limit (Optional[int]): The number of returned result sets. Default: 50, maximum: 100. Defaults to None.
            recv_window (Optional[int]): Request valid time window value, Unit: milliseconds. Defaults to None.

        Returns:
            SwapQueryHistoricalTransactionOrdersResponse: The response data.

        """
        params: dict[str, Any] = {}
        if from_id is not None:
            params["fromId"] = from_id
        if symbol is not None:
            params["symbol"] = symbol
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/market/historicalTrades", params=params),
            SwapQueryHistoricalTransactionOrdersResponse,
        )

    def symbol_order_book_ticker(
        self,
        symbol: str,
        recv_window: Optional[int] = None,
    ) -> SymbolOrderBookTickerResponse:
        """Symbol Order Book Ticker.

        Args:
            symbol (str): Trading pair, for example: BTC-USDT.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            SymbolOrderBookTickerResponse: The response data.

        """
        params: dict[str, Any] = {"symbol": symbol}
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v2/quote/bookTicker", params=params),
            SymbolOrderBookTickerResponse,
        )

    def mark_price_kline_candlestick_data(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> MarkPriceKlineCandlestickDataResponse:
        """Mark Price Kline/Candlestick Data.

        Args:
            symbol (str): Trading pair, for example: BTC-USDT.
            interval (str): Time interval, refer to field description.
            start_time (Optional[int]): Start time, unit: millisecond. Defaults to None.
            end_time (Optional[int]): End time, unit: millisecond. Defaults to None.
            limit (Optional[int]): Default: 500, maximum: 1440. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            MarkPriceKlineCandlestickDataResponse: The response data.

        """
        params: dict[str, Any] = {"symbol": symbol, "interval": interval}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/market/markPriceKlines", params=params),
            MarkPriceKlineCandlestickDataResponse,
        )

    def symbol_price_ticker(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> SwapSymbolPriceTickerResponse:
        """Symbol Price Ticker.

        Args:
            symbol (Optional[str]): Trading pair, for example: BTC-USDT. If no transaction pair parameters are sent, all transaction pair information will be returned. Defaults to None.
            recv_window (Optional[int]): Timestamp of initiating the request, Unit: milliseconds. Defaults to None.

        Returns:
            SwapSymbolPriceTickerResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            self.client.get("/openApi/swap/v1/ticker/price", params=params),
            SwapSymbolPriceTickerResponse,
        )
