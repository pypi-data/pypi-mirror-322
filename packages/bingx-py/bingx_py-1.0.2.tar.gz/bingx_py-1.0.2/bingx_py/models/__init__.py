"""BingX API Models.

This package contains Pydantic models for representing data related to the BingX API.
These models are used to validate and serialize responses from the BingX API.

Classes:
    - Various models representing different types of data from the BingX API.
"""

from pydantic import BaseModel, Field


class GenerateListenKeyResponse(BaseModel):
    """Model for the response data of GenerateListenKey.

    Args:
        listen_key (str): The generated listen key.

    """

    listen_key: str = Field(..., alias="listenKey")


class QueryApiKeyRestrictionsResponse(BaseModel):
    """Model for the response data of QueryApiKeyRestrictions.

    Args:
        ip_restrict (bool): Whether to restrict IP access.
        create_time (int): Creation time.
        permits_universal_transfer (bool): Authorize the key to be used on a dedicated universal transfer interface.
        enable_reading (bool): Can read.
        enable_futures (bool): Swap trading authority.
        enable_spot_and_margin_trading (bool): Spot authority.

    """

    ip_restrict: bool = Field(..., alias="ipRestrict")
    create_time: int = Field(..., alias="createTime")
    permits_universal_transfer: bool = Field(..., alias="permitsUniversalTransfer")
    enable_reading: bool = Field(..., alias="enableReading")
    enable_futures: bool = Field(..., alias="enableFutures")
    enable_spot_and_margin_trading: bool = Field(
        ...,
        alias="enableSpotAndMarginTrading",
    )


class QueryApiKeyPermissionsResponse(BaseModel):
    """Model for the response data of QueryApiKeyPermissions.

    Args:
        api_key (str): API key.
        permissions (List[int]): Permissions list. 1-spot trading, 2-reading, 3-professional contract trading, 4-universal transfer, 5-coin withdrawal, 7-allow transfer within sub-account
        ip_addresses (List[str]): IP whitelist.
        note (str): Remark.

    """

    api_key: str = Field(..., alias="apiKey")
    permissions: list[int]
    ip_addresses: list[str] = Field(..., alias="ipAddresses")
    note: str
