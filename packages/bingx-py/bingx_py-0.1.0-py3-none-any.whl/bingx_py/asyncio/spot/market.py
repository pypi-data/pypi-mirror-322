from typing import TYPE_CHECKING, Any, Optional

from bingx_py.models.spot.market import (
    HistoricalKlineResponse,
    KlineDataResponse,
    OldTradeLookupResponse,
    OrderBookAggregationResponse,
    OrderBookResponse,
    RecentTradesListResponse,
    SpotSymbolOrderBookTickerResponse,
    SpotTradingSymbolsResponse,
    SymbolPriceTickerResponse,
    Ticker24hrResponse,
)

if TYPE_CHECKING:
    from bingx_py.asyncio import BingXHttpClient


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

    async def get_spot_trading_symbols(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> SpotTradingSymbolsResponse:
        """Get spot trading symbols.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            SpotTradingSymbolsResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/spot/v1/common/symbols",
                params=params,
            ),
            SpotTradingSymbolsResponse,
        )

    async def get_recent_trades_list(
        self,
        symbol: str,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> RecentTradesListResponse:
        """Get recent trades list.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            limit (Optional[int]): Default 100, max 500. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            RecentTradesListResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/spot/v1/market/trades",
                params=params,
            ),
            RecentTradesListResponse,
        )

    async def get_order_book(
        self,
        symbol: str,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> OrderBookResponse:
        """Get order book.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            limit (Optional[int]): Default 20, max 1000. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            OrderBookResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/spot/v1/market/depth", params=params),
            OrderBookResponse,
        )

    async def get_kline_data(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
        recv_window: Optional[int] = None,
    ) -> KlineDataResponse:
        """Get Kline/Candlestick data.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            interval (str): Time interval, refer to field description.
            start_time (Optional[int]): Start time, unit: milliseconds. Defaults to None.
            end_time (Optional[int]): End time, unit: milliseconds. Defaults to None.
            limit (Optional[int]): Default value: 500, maximum value: 1440. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            KlineDataResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "interval": interval,
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/spot/v2/market/kline", params=params),
            KlineDataResponse,
        )

    async def get_24hr_ticker_price_change_statistics(
        self,
        symbol: Optional[str] = None,
        recv_window: Optional[int] = None,
    ) -> Ticker24hrResponse:
        """Get 24hr ticker price change statistics.

        Args:
            symbol (Optional[str]): Trading pair, e.g., BTC-USDT. Defaults to None.
            recv_window (Optional[int]): Request valid time window, unit: milliseconds. Defaults to None.

        Returns:
            Ticker24hrResponse: The response data.

        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.client.save_convert(
            await self.client.async_get("/openApi/spot/v1/ticker/24hr", params=params),
            Ticker24hrResponse,
        )

    async def get_order_book_aggregation(
        self,
        symbol: str,
        depth: int,
        precision_type: str,
    ) -> OrderBookAggregationResponse:
        """Get order book aggregation.

        Args:
            symbol (str): Trading pair, e.g., BTC_USDT.
            depth (int): Query depth.
            precision_type (str): Precision type (step0, step1, step2, step3, step4, step5).

        Returns:
            OrderBookAggregationResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "depth": depth,
            "type": precision_type,
        }

        return self.client.save_convert(
            await self.client.async_get("/openApi/spot/v2/market/depth", params=params),
            OrderBookAggregationResponse,
        )

    async def get_symbol_price_ticker(
        self,
        symbol: str,
    ) -> SymbolPriceTickerResponse:
        """Get symbol price ticker.

        Args:
        symbol (str): Trading pair, e.g., BTC_USDT.

        Returns:
        SymbolPriceTickerResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }

        return self.client.save_convert(
            await self.client.async_get("/openApi/spot/v1/ticker/price", params=params),
            SymbolPriceTickerResponse,
        )

    async def get_symbol_order_book_ticker(
        self,
        symbol: str,
    ) -> SpotSymbolOrderBookTickerResponse:
        """Get symbol order book ticker.

        Args:
        symbol (str): Trading pair, e.g., BTC_USDT.

        Returns:
        SpotSymbolOrderBookTickerResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }

        return self.client.save_convert(
            await self.client.async_get(
                "/openApi/spot/v1/ticker/bookTicker",
                params=params,
            ),
            SpotSymbolOrderBookTickerResponse,
        )

    async def get_historical_kline(
        self,
        symbol: str,
        interval: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> HistoricalKlineResponse:
        """Get historical K-line data.

        Args:
        symbol (str): Trading pair, e.g., BTC-USDT.
        interval (str): Time interval.
        start_time (Optional[int]): Start time, unit: milliseconds. Defaults to None.
        end_time (Optional[int]): End time, unit: milliseconds. Defaults to None.
        limit (Optional[int]): Default value: 500, maximum value: 500. Defaults to None.

        Returns:
        HistoricalKlineResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "interval": interval,
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit

        return self.client.save_convert(
            await self.client.async_get("/openApi/market/his/v1/kline", params=params),
            HistoricalKlineResponse,
        )

    async def get_old_trade_lookup(
        self,
        symbol: str,
        limit: Optional[int] = None,
        from_id: Optional[str] = None,
    ) -> OldTradeLookupResponse:
        """Get old trade lookup.

        Args:
            symbol (str): Trading pair, e.g., BTC-USDT.
            limit (Optional[int]): Default 100, maximum 500. Defaults to None.
            from_id (Optional[str]): The last recorded trade ID. Defaults to None.

        Returns:
            OldTradeLookupResponse: The response data.

        """
        params: dict[str, Any] = {
            "symbol": symbol,
        }
        if limit is not None:
            params["limit"] = limit
        if from_id is not None:
            params["fromId"] = from_id

        return self.client.save_convert(
            await self.client.async_get("/openApi/market/his/v1/trade", params=params),
            OldTradeLookupResponse,
        )
