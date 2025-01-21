from typing import Any, Optional

from pydantic import BaseModel


class APIError(Exception):
    """Represents an error returned by the API.

    Args:
        code (int): The error code.
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(
        self,
        code: int,
        message: str,
        timestamp: Optional[int] = None,
    ) -> None:
        self.code = code
        self.message = message
        self.timestamp = timestamp
        super().__init__(
            f"API Error {code}: {message}"
            + (f" (Timestamp: {timestamp})" if timestamp is not None else ""),
        )

    def __repr__(self) -> str:
        """Representation of the exception.

        Returns
        -------
            str: The string representation of the exception.

        """
        return (
            f"APIError(code={self.code}, message={self.message!r}, "
            f"timestamp={self.timestamp!r})"
        )


# 4XX Errors
class BadRequestError(APIError):
    """Raised when the request is invalid or malformed.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(400, message, timestamp)


class UnauthorizedError(APIError):
    """Raised when the request is unauthorized (e.g., invalid API key).

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(401, message, timestamp)


class ForbiddenError(APIError):
    """Raised when access to the requested resource is forbidden.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(403, message, timestamp)


class NotFoundError(APIError):
    """Raised when the requested resource is not found.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(404, message, timestamp)


class TooManyRequestsError(APIError):
    """Raised when the request rate limit is exceeded.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(429, message, timestamp)


class IPBannedError(APIError):
    """Raised when the IP is banned due to excessive requests.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(418, message, timestamp)


# 5XX Errors
class InternalServerError(APIError):
    """Raised when there is an internal server error.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(500, message, timestamp)


class GatewayTimeoutError(APIError):
    """Raised when the API server fails to get a response from the service center.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(504, message, timestamp)


# Common Business Errors
class SignatureVerificationFailedError(APIError):
    """Raised when the signature verification fails.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100001, message, timestamp)


class InternalSystemError(APIError):
    """Raised when there is an internal system error.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100500, message, timestamp)


class OperationError(APIError):
    """Raised when the service is unavailable.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80012, message, timestamp)


class InvalidParameterError(APIError):
    """Raised when an invalid parameter is provided.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80014, message, timestamp)


class OrderNotFoundError(APIError):
    """Raised when the specified order does not exist.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80016, message, timestamp)


class PositionNotFoundError(APIError):
    """Raised when the specified position does not exist.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80017, message, timestamp)


class RiskForbiddenError(APIError):
    """Raised when the request is forbidden due to risk control.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80020, message, timestamp)


class PermissionDeniedError(APIError):
    """Raised when the API key does not have the required permissions.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100004, message, timestamp)


class IPWhitelistError(APIError):
    """Raised when the IP does not match the whitelist.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100419, message, timestamp)


class InsufficientMarginError(APIError):
    """Raised when there is insufficient margin to perform the operation.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101204, message, timestamp)


class OrderLimitReachedError(APIError):
    """Raised when the number of orders exceeds the system limit.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80013, message, timestamp)


class OrderAlreadyFilledError(APIError):
    """Raised when the order is already filled.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80018, message, timestamp)


class OrderProcessingError(APIError):
    """Raised when the order is still being processed.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80019, message, timestamp)


class NullSignatureError(APIError):
    """Raised when the signature is null.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100412, message, timestamp)


class IncorrectAPIKeyError(APIError):
    """Raised when the API key is incorrect.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100413, message, timestamp)


class TimestampError(APIError):
    """Raised when the timestamp is null or mismatched.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100421, message, timestamp)


class RateLimitError(APIError):
    """Raised when the rate limit is exceeded.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(100410, message, timestamp)


class MaxPositionValueError(APIError):
    """Raised when the position value exceeds the maximum allowed for the leverage.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101209, message, timestamp)


class PendingOrdersError(APIError):
    """Raised when there are pending orders that need to be canceled.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101212, message, timestamp)


class MakerOrderError(APIError):
    """Raised when a Maker (Post Only) order would immediately match with available orders.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101215, message, timestamp)


class MaxLeverageError(APIError):
    """Raised when the leverage exceeds the maximum allowed for the trading pair.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101414, message, timestamp)


class TradingPairSuspendedError(APIError):
    """Raised when the trading pair is suspended from opening new positions.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101415, message, timestamp)


class LiquidationPriceError(APIError):
    """Raised when the order price is below the estimated liquidation price.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101460, message, timestamp)


class RPCTimeoutError(APIError):
    """Raised when an RPC request times out.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101500, message, timestamp)


class SuspendedFromOpeningPositionsError(APIError):
    """Raised when the user is temporarily suspended from opening positions.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101514, message, timestamp)


class DuplicateOrderError(APIError):
    """Raised when the same order number is submitted multiple times within 1 second.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(109201, message, timestamp)


class OrderPriceError(APIError):
    """Raised when the order price is outside the allowed range.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101211, message, timestamp)


class TradeValidationError(APIError):
    """Raised when there is no position to close.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(101400, message, timestamp)


class TradeExecutionError(APIError):
    """Raised when the connection is invalid.

    Args:
        message (str): The error message.
        timestamp (Optional[int]): The timestamp of the error. Defaults to None.

    Returns:
        None

    """

    def __init__(self, message: str, timestamp: Optional[int] = None) -> None:
        super().__init__(80001, message, timestamp)


class ConversionError(Exception):
    """Raised when the conversion to the model type fails.

    Args:
        initial_data (dict[str, Any]): The initial data that failed to convert.
        model_type (type[BaseModel]): The model type that was attempted to convert to.

    Returns:
        None

    """

    def __init__(
        self,
        initial_data: dict[str, Any],
        model_type: type[BaseModel],
    ) -> None:
        self.initial_data = initial_data
        self.model_type = model_type

    def __repr__(self) -> str:
        """Representation of the exception.

        Returns
        -------
            str: The string representation of the exception.

        """
        return (
            f"{self.__class__.__name__}(initial_data={str(self.initial_data)[:300]}, "
            f"model_type={self.model_type!r})"
        )

    def __str__(self) -> str:
        """Representation of the exception.

        Returns
        -------
            str: The string representation of the exception.

        """
        return (
            f"ConversionError: Failed to convert {str(self.initial_data)[:300]}... to {self.model_type.__name__}"
            f""
        )
