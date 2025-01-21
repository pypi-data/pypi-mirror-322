from enum import Enum

from pydantic import BaseModel, Field


class OrderSide(str, Enum):
    """Enum for order sides.

    Args:
        BUY (str): Buy order.
        SELL (str): Sell order.

    """

    BUY = "BUY"
    SELL = "SELL"


class TimeInForce(str, Enum):
    """Enum for time in force options.

    Args:
        POST_ONLY (str): Post-only order (will not execute immediately).
        GTC (str): Good 'til canceled (order remains active until canceled).
        IOC (str): Immediate or cancel (order executes immediately or is canceled).
        FOK (str): Fill or kill (order must be filled immediately or canceled).

    """

    POST_ONLY = "PostOnly"
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class OrderStatus(str, Enum):
    """Enum for order statuses.

    Args:
        NEW (str): The order has been accepted by the system.
        PENDING (str): The order is pending execution.
        PARTIALLY_FILLED (str): The order has been partially filled.
        FILLED (str): The order has been fully filled.
        CANCELED (str): The order has been canceled.
        FAILED (str): The order has failed.

    """

    NEW = "NEW"
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    FAILED = "FAILED"


class MainAccountInternalTransferResponseData(BaseModel):
    """Model for the data field in MainAccountInternalTransferResponse.

    Args:
        id (str): The platform returns the unique ID of the internal transfer record.

    """

    id: str = Field(
        ...,
        description="The platform returns the unique ID of the internal transfer record",
    )


class MainAccountInternalTransferResponse(BaseModel):
    """Model for the response of Main Account Internal Transfer.

    Args:
        code (int): Error code, 0 means successful response, others mean response failure.
        timestamp (int): Response timestamp.
        data (MainAccountInternalTransferResponseData): Response data.

    """

    code: int = Field(
        ...,
        description="Error code, 0 means successful response, others mean response failure",
    )
    timestamp: int = Field(..., description="Response timestamp")
    data: MainAccountInternalTransferResponseData = Field(
        ...,
        description="Response data",
    )
