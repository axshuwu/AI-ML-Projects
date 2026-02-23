"""
Binance Futures Trading Bot
A clean, professional trading bot for Binance Futures Testnet
"""

from .client import BinanceFuturesClient
from .orders import OrderManager
from .validators import InputValidator, ValidationError
from .logging_config import setup_logging, get_logger

__version__ = "1.0.0"
__all__ = [
    'BinanceFuturesClient',
    'OrderManager',
    'InputValidator',
    'ValidationError',
    'setup_logging',
    'get_logger'
]
