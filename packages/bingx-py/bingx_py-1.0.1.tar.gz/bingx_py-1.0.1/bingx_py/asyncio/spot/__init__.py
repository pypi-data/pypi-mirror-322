"""Spot Trading API for BingX.

This module provides a comprehensive API for interacting with BingX's spot trading features.
It includes functionalities for account management, market data retrieval, trade execution,
and wallet operations.

Classes:
    - `SpotAPI`: Combines `AccountAPI`, `MarketAPI`, `TradesAPI`, and `WalletAPI` to provide
      a unified interface for managing spot trading on BingX.
"""

from bingx_py.asyncio.spot.account import AccountAPI
from bingx_py.asyncio.spot.market import MarketAPI
from bingx_py.asyncio.spot.trades import TradesAPI
from bingx_py.asyncio.spot.wallet import WalletAPI


class SpotAPI(AccountAPI, MarketAPI, TradesAPI, WalletAPI):
    """API for managing spot trading on BingX.

    This class combines functionalities from `AccountAPI`, `MarketAPI`, `TradesAPI`, and `WalletAPI`
    to provide a unified interface for managing spot trading, including account data, market data,
    trade execution, and wallet operations.
    """
