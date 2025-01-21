from __future__ import annotations
import hashlib
import hmac
import logging
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Literal
from urllib import parse

import aiohttp
import requests
from pydantic import BaseModel, ValidationError
from typing_extensions import Self

from bingx_py.config import cache_config

from . import exceptions
from .caching.base import BaseAsyncCache, BaseCache

if TYPE_CHECKING:
    from types import TracebackType

HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]

logger = logging.getLogger("bingx-py")


class HttpClient(ABC):
    """Base class for HTTP clients with caching support."""

    def __init__(
        self,
        base_url: str,
        cache: BaseCache | BaseAsyncCache | None = None,
        default_cache_ttl: int = 300,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            base_url (str): The base URL of the API.
            cache (Optional[BaseCache | BaseAsyncCache]): The cache instance to use. If not provided, the global cache is used.
            default_cache_ttl (int): The default time-to-live (TTL) for cached data in seconds. Defaults to 300 seconds.

        Returns:
            None

        """
        self.base_url = base_url
        self.cache = cache if cache else cache_config.get_cache()
        self.default_cache_ttl = default_cache_ttl
        self._session: requests.Session | None = None
        self._async_session: aiohttp.ClientSession | None = None

    def connect(self) -> None:
        """Initialize the synchronous HTTP session.

        Returns:
            None

        """
        logger.debug("Initializing synchronous session.")
        self._session = requests.Session()

    def close(self) -> None:
        """Close the synchronous HTTP session.

        Returns
        -------
            None

        """
        if self._session:
            logger.debug("Closing synchronous session.")
            self._session.close()

    async def connect_async(self) -> None:
        """Initialize the asynchronous HTTP session.

        Returns
        -------
            None

        """
        logger.debug("Initializing asynchronous session.")
        self._async_session = aiohttp.ClientSession()

    async def close_async(self) -> None:
        """Close the asynchronous HTTP session.

        Returns
        -------
            None

        """
        if self._async_session:
            logger.debug("Closing asynchronous session.")
            await self._async_session.close()

    def __enter__(self) -> Self:
        """Enter the synchronous context manager and initialize the session.

        Returns
        -------
            Self: The instance of the HTTP client.

        """
        logger.debug("Entering synchronous context manager.")
        self._session = requests.Session()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the synchronous context manager and close the session.

        Args:
            exc_type (Optional[Type[BaseException]]): The exception type, if any.
            exc (Optional[BaseException]): The exception instance, if any.
            tb (Optional[TracebackType]): The traceback, if any.

        Returns:
            None

        """
        logger.debug("Exiting synchronous context manager.")
        if self._session:
            self._session.close()

    async def __aenter__(self) -> Self:
        """Enter the asynchronous context manager and initialize the session.

        Returns
        -------
            Self: The instance of the HTTP client.

        """
        logger.debug("Entering asynchronous context manager.")
        self._async_session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the asynchronous context manager and close the session.

        Args:
            exc_type (Optional[Type[BaseException]]): The exception type, if any.
            exc (Optional[BaseException]): The exception instance, if any.
            tb (Optional[TracebackType]): The traceback, if any.

        Returns:
            None

        """
        logger.debug("Exiting asynchronous context manager.")
        if self._async_session:
            await self._async_session.close()

    def _generate_cache_key(
        self,
        method: HttpMethod,
        endpoint: str,
        params: dict[str, Any] | None = None,
        unique_cache_attribute: str | None = None,
    ) -> str:
        """Generate a unique cache key based on the request details.

        Args:
            method (HttpMethod): The HTTP method (e.g., GET, POST).
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.

        Returns:
            str: A unique cache key.

        """
        key_parts = [method, endpoint]
        if params:
            key_parts.append(parse.urlencode(sorted(params.items())))
        if unique_cache_attribute:
            key_parts.append(unique_cache_attribute)
        cache_key = ":".join(key_parts)
        logger.debug(f"Generated cache key: {cache_key}")
        return cache_key

    def _request(
        self,
        method: HttpMethod,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = False,
        unique_cache_attribute: str | None = None,
    ) -> dict[str, Any]:
        """Perform a synchronous HTTP request with optional caching.

        Args:
            method (HttpMethod): The HTTP method (e.g., GET, POST).
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.
            use_cache (bool): Whether to use caching for the request. Defaults to False.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.

        Returns:
            Dict[str, Any]: The response data.

        Raises:
        ------
            RuntimeError: If the synchronous session is not initialized.
            ValueError: If caching is attempted for non-GET requests without enabling unsafe caching.

        """
        if not self._session:
            msg = "Synchronous session is not initialized. Use context manager (with)."
            raise RuntimeError(
                msg,
            )

        if use_cache and method != "GET" and not cache_config.is_unsafe_cache_enabled():
            msg = "Cache is supported only for GET requests. If you want to cache data with another method, use config.enable_unsafe_cache"
            raise ValueError(
                msg,
            )

        # bound `cache_key` to None to avoid generate cache key without `use_cache`
        cache_key = None

        # Try to get data from cache
        if use_cache:
            if self.cache:
                if isinstance(self.cache, BaseCache):
                    # Generate cache key
                    cache_key = self._generate_cache_key(
                        method,
                        endpoint,
                        params,
                        unique_cache_attribute,
                    )
                    logger.debug(f"Checking cache for key: {cache_key}")
                    if (cached_data := self.cache.get(cache_key)) is not None:
                        logger.debug("Cache hit. Returning cached data.")
                        return cached_data
                else:
                    logger.warning(
                        "Can`t use async cache. You made a synchronous request with an async cache. Consider providing an async cache via the `cache` parameter or setting it globally in the config.",
                    )
            else:
                logger.warning(
                    "Can`t use cache cause cache instance doesn`t set up via the `cache` parameter or via globally setting in the config.",
                )

        # Make request
        url = f"{self.base_url}{endpoint}"
        logger.debug(
            f"Making {method} request to {url} with params: {params}",
        )
        response = self._session.request(
            method,
            url,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        try:
            data = response.json()
        except requests.JSONDecodeError:
            data: dict[str, Any] = {}

        logger.debug(f"Response\nUrl: {response.url}\nData: {data}")
        self._check_errors(data)

        # Save data to cache
        if use_cache and self.cache and isinstance(self.cache, BaseCache) and cache_key:
            logger.debug(f"Saving data to cache with key: {cache_key}")
            self.cache.set(cache_key, data, ttl=self.default_cache_ttl)

        return data

    async def _async_request(
        self,
        method: HttpMethod,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = False,
        unique_cache_attribute: str | None = None,
    ) -> dict[str, Any]:
        """Perform an asynchronous HTTP request with optional caching.

        Args:
            method (HttpMethod): The HTTP method (e.g., GET, POST).
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.
            use_cache (bool): Whether to use caching for the request. Defaults to False.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.

        Returns:
            Dict[str, Any]: The response data.

        Raises:
        ------
            RuntimeError: If the asynchronous session is not initialized.
            ValueError: If caching is attempted for non-GET requests without enabling unsafe caching.

        """
        if not self._async_session:
            msg = "Asynchronous session is not initialized. Use context manager (async with)."
            raise RuntimeError(
                msg,
            )

        # bound `cache_key` to None to avoid generate cache key without `use_cache`
        cache_key = None

        if use_cache and method != "GET" and not cache_config.is_unsafe_cache_enabled():
            msg = "Cache is supported only for GET requests. If you want to cache data with another method, use need to invoke `config.enable_unsafe_cache`"
            raise ValueError(
                msg,
            )

        # Try to get data from cache
        if use_cache:
            if self.cache:
                # Generate cache key
                cache_key = self._generate_cache_key(
                    method,
                    endpoint,
                    params,
                    unique_cache_attribute,
                )
                if isinstance(self.cache, BaseAsyncCache):
                    logger.debug(f"Checking async cache for key: {cache_key}")
                    if (cached_data := await self.cache.aget(cache_key)) is not None:
                        logger.debug("Cache hit. Returning cached data.")
                        return cached_data
                else:
                    logger.warning(
                        "You made a asynchronous request with an sync cache. This may be slower. Consider providing an async cache via the `cache` parameter or setting it globally in the config.",
                    )
                    if (cached_data := self.cache.get(cache_key)) is not None:
                        logger.debug("Cache hit. Returning cached data.")
                        return cached_data
            else:
                logger.warning(
                    "Can`t use cache cause cache instance doesn`t set up via the `cache` parameter or via globally setting in the config.",
                )

        # Make request
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Making async {method} request to {url} with params: {params}")
        async with self._async_session.request(
            method,
            url,
            params=params,
            headers=headers,
        ) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)
            logger.debug(f"Recieve response with data:\n{data}")
            self._check_errors(data or {})

            # Save data to cache
            if use_cache and self.cache and cache_key is not None:
                if isinstance(self.cache, BaseAsyncCache):
                    logger.debug(f"Saving data to async cache with key: {cache_key}")
                    await self.cache.aset(cache_key, data, ttl=self.default_cache_ttl)
                else:
                    logger.warning(
                        "You made a asynchronous request with an sync cache. This may be slower. Consider providing an async cache via the `cache` parameter or setting it globally in the config.",
                    )
                    logger.debug(f"Saving data to sync cache with key: {cache_key}")
                    self.cache.set(cache_key, data, ttl=self.default_cache_ttl)

            return data

    @abstractmethod
    def _check_errors(self, data: dict[str, Any]) -> None:
        """Check the API response for errors and raise exceptions if necessary.

        Args:
            data (Dict[str, Any]): The parsed response data from the API.

        Raises:
        ------
            NotImplementedError: If the method is not implemented in a subclass.

        """
        msg = "Method _check_errors must be implemented"
        raise NotImplementedError(msg)


class BingXHttpClient(HttpClient):
    """HTTP client for interacting with the BingX API."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str,
        cache: BaseCache | BaseAsyncCache | None = None,
        default_cache_ttl: int = 300,
    ) -> None:
        """Initialize the BingX HTTP client.

        Args:
            api_key (str): The API key for authentication.
            api_secret (str): The API secret for signing requests.
            base_url (str): The base URL of the BingX API.
            cache (Optional[BaseCache | BaseAsyncCache]): The cache instance to use. If not provided, the global cache is used.
            default_cache_ttl (int): The default time-to-live (TTL) for cached data in seconds. Defaults to 300 seconds.

        Returns:
            None

        """
        self._api_key = api_key
        self._api_secret = api_secret
        super().__init__(base_url, cache, default_cache_ttl)

    def _parse_params(self, params: dict[str, Any]) -> str:
        """Parse request parameters to a string.

        Args:
            params (Dict[str, Any]): The request parameters.

        Returns:
            str: The request parameters as serialized string.

        """
        params_string = "&".join(
            f"{k}={str(v).replace(' ', '') if isinstance(v, list) else v}"  # type: ignore
            for k, v in sorted(params.items())
            if v
        )
        if params_string != "":
            return params_string + "&timestamp=" + str(int(time.time() * 1000))
        return params_string + "timestamp=" + str(int(time.time() * 1000))

    def _sign_request(self, params_str: str) -> str:
        """Prepare and sign the request parameters.

        Args:
            params_str (str): The request parameters as serialized string.

        Returns:
            str: The signature of request parameters.

        """
        # Generate HMAC SHA256 signature
        return hmac.new(
            self._api_secret.encode("utf-8"),
            params_str.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _generate_cache_key(
        self,
        method: HttpMethod,
        endpoint: str,
        params: dict[str, Any] | None = None,
        unique_cache_attribute: str | None = None,
    ) -> str:
        """Generate a unique cache key based on the request details.

        Exclude timestamp and signature from the cache key.

        Args:
            method (HttpMethod): The HTTP method (e.g., GET, POST).
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.

        Returns:
            str: A unique cache key.

        """
        key_parts = [method, endpoint]
        if params:
            filtered_params = {
                k: v for k, v in params.items() if k not in {"signature", "timestamp"}
            }
            key_parts.append(parse.urlencode(sorted(filtered_params.items())))
        if unique_cache_attribute:
            key_parts.append(unique_cache_attribute)
        cache_key = ":".join(key_parts)
        logger.debug(f"Generated cache key: {cache_key}")
        return cache_key

    def _request(
        self,
        method: HttpMethod,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = False,
        unique_cache_attribute: str | None = None,
        override_signature: Callable[[str], str] | None = None,
    ) -> dict[str, Any]:
        """Perform a signed synchronous HTTP request.

        Args:
            method (HttpMethod): The HTTP method (e.g., GET, POST).
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.
            use_cache (bool): Whether to use caching for the request. Defaults to False.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.
            override_signature (Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]): An optional function to override the default signing behavior.

        Returns:
            Dict[str, Any]: The response data.

        """
        headers = headers or {}
        headers["X-BX-APIKEY"] = self._api_key

        params = params or {}
        params_str = self._parse_params(params)
        if override_signature:
            signature = override_signature(params_str)
        else:
            signature = self._sign_request(params_str)

        endpoint += f"?{params_str}&signature={signature}"

        return super()._request(
            method,
            endpoint,
            headers=headers,
            use_cache=use_cache,
            unique_cache_attribute=unique_cache_attribute,
        )

    async def _async_request(
        self,
        method: HttpMethod,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = False,
        unique_cache_attribute: str | None = None,
        override_signature: Callable[[str], str] | None = None,
    ) -> dict[str, Any]:
        """Perform a signed asynchronous HTTP request.

        Args:
            method (HttpMethod): The HTTP method (e.g., GET, POST).
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.
            use_cache (bool): Whether to use caching for the request. Defaults to False.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.
            override_signature (Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]): An optional function to override the default signing behavior.

        Returns:
            Dict[str, Any]: The response data.

        """
        headers = headers or {}
        headers["X-BX-APIKEY"] = self._api_key

        params = params or {}
        params_str = self._parse_params(params)
        if override_signature:
            signature = override_signature(params_str)
        else:
            signature = self._sign_request(params_str)

        endpoint += f"?{params_str}&signature={signature}"

        return await super()._async_request(
            method,
            endpoint,
            headers=headers,
            use_cache=use_cache,
            unique_cache_attribute=unique_cache_attribute,
        )

    def _check_errors(self, data: dict[str, Any]) -> None:
        """Check the API response for errors and raise exceptions if necessary.

        Args:
            data (Dict[str, Any]): The parsed response data from the API.

        Raises:
        ------
            exceptions.APIError: If the API response contains an error.

        """
        if "code" not in data or data["code"] == 0:
            return  # No error

        error_code = data["code"]
        error_message = data.get("msg", "No error message provided")
        timestamp = data.get("timestamp")
        logger.debug(
            f"API error detected. Code: {error_code}, Message: {error_message}, Timestamp: {timestamp}",
        )

        # Map error codes to specific exception classes
        error_mapping: dict[int, type[exceptions.APIError]] = {
            # 4XX Errors
            400: exceptions.BadRequestError,
            401: exceptions.UnauthorizedError,
            403: exceptions.ForbiddenError,
            404: exceptions.NotFoundError,
            429: exceptions.TooManyRequestsError,
            418: exceptions.IPBannedError,
            # 5XX Errors
            500: exceptions.InternalServerError,
            504: exceptions.GatewayTimeoutError,
            # Common Business Errors
            100001: exceptions.SignatureVerificationFailedError,
            100500: exceptions.InternalSystemError,
            80012: exceptions.OperationError,
            80014: exceptions.InvalidParameterError,
            80016: exceptions.OrderNotFoundError,
            80017: exceptions.PositionNotFoundError,
            80020: exceptions.RiskForbiddenError,
            100004: exceptions.PermissionDeniedError,
            100419: exceptions.IPWhitelistError,
            101204: exceptions.InsufficientMarginError,
            80013: exceptions.OrderLimitReachedError,
            80018: exceptions.OrderAlreadyFilledError,
            80019: exceptions.OrderProcessingError,
            100412: exceptions.NullSignatureError,
            100413: exceptions.IncorrectAPIKeyError,
            100421: exceptions.TimestampError,
            100410: exceptions.RateLimitError,
            101209: exceptions.MaxPositionValueError,
            101212: exceptions.PendingOrdersError,
            101215: exceptions.MakerOrderError,
            101414: exceptions.MaxLeverageError,
            101415: exceptions.TradingPairSuspendedError,
            101460: exceptions.LiquidationPriceError,
            101500: exceptions.RPCTimeoutError,
            101514: exceptions.SuspendedFromOpeningPositionsError,
            109201: exceptions.DuplicateOrderError,
            101211: exceptions.OrderPriceError,
            101400: exceptions.TradeValidationError,
            80001: exceptions.TradeExecutionError,
        }

        # Get the appropriate exception class or fall back to the base APIError
        exception_class = error_mapping.get(error_code, exceptions.APIError)

        # Raise the exception with the error message and timestamp
        if exception_class == exceptions.APIError:
            raise exception_class(
                message=error_message,
                timestamp=timestamp,
                code=error_code,
            )
        raise exception_class(message=error_message, timestamp=timestamp)  # type: ignore

    # ------------------------------
    # HTTP Method Shortcuts (Synchronous)
    # ------------------------------

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = False,
        unique_cache_attribute: str | None = None,
    ) -> dict[str, Any]:
        """Perform a synchronous GET request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.
            use_cache (bool): Whether to use caching for the request. Defaults to False.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.

        Returns:
            Dict[str, Any]: The response data.

        """
        return self._request(
            "GET",
            endpoint,
            params=params,
            headers=headers,
            use_cache=use_cache,
            unique_cache_attribute=unique_cache_attribute,
        )

    def post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Perform a synchronous POST request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.

        Returns:
            Dict[str, Any]: The response data.

        """
        return self._request(
            "POST",
            endpoint,
            params=params,
            headers=headers,
        )

    def put(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Perform a synchronous PUT request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.

        Returns:
            Dict[str, Any]: The response data.

        """
        return self._request(
            "PUT",
            endpoint,
            params=params,
            headers=headers,
        )

    def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Perform a synchronous DELETE request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.

        Returns:
            Dict[str, Any]: The response data.

        """
        return self._request(
            "DELETE",
            endpoint,
            params=params,
            headers=headers,
        )

    # ------------------------------
    # HTTP Method Shortcuts (Asynchronous)
    # ------------------------------

    async def async_get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = False,
        unique_cache_attribute: str | None = None,
    ) -> dict[str, Any]:
        """Perform an asynchronous GET request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.
            use_cache (bool): Whether to use caching for the request. Defaults to False.
            unique_cache_attribute (Optional[str]): An optional unique attribute for the cache key.

        Returns:
            Dict[str, Any]: The response data.

        """
        return await self._async_request(
            "GET",
            endpoint,
            params=params,
            headers=headers,
            use_cache=use_cache,
            unique_cache_attribute=unique_cache_attribute,
        )

    async def async_post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Perform an asynchronous POST request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.

        Returns:
            Dict[str, Any]: The response data.

        """
        return await self._async_request(
            "POST",
            endpoint,
            params=params,
            headers=headers,
        )

    async def async_put(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Perform an asynchronous PUT request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.

        Returns:
            Dict[str, Any]: The response data.

        """
        return await self._async_request(
            "PUT",
            endpoint,
            params=params,
            headers=headers,
        )

    async def async_delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Perform an asynchronous DELETE request.

        Args:
            endpoint (str): The API endpoint.
            params (Optional[Dict[str, Any]]): The request parameters.
            headers (Optional[Dict[str, str]]): The request headers.

        Returns:
            Dict[str, Any]: The response data.

        """
        return await self._async_request(
            "DELETE",
            endpoint,
            params=params,
            headers=headers,
        )

    def save_convert(
        self,
        data: dict[str, Any],
        pydantic_model: type[BaseModel],
    ) -> Any:
        """Convert response data to a specified Pydantic model.

        Args:
            data (Dict[str, Any]): The data to be converted.
            pydantic_model (Type[BaseModel]): The Pydantic model class for conversion.

        Returns:
            Any: An instance of the provided Pydantic model.

        Raises:
            ConversionError: If conversion to the Pydantic model fails due to validation errors.

        """
        try:
            return pydantic_model(**data)
        except ValidationError as e:
            logger.warning(f"Failed to convert data: {e}.")
            logger.warning("nRaising ConversionError with initial data.")
            raise exceptions.ConversionError(data, pydantic_model) from e
