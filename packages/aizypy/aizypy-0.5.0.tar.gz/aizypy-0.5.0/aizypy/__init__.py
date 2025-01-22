"""
AIZYClientPy - A Python framework for creating and testing trading bots
"""

from .CandleData import CandleData
from .OrderManager import OrderManager, OrderStatus, Order
from .TestEngine import TestEngine
from .Trade import Trade
from .WebSocketHandler import WebSocketHandler
from .AizyBot import TradingPair, LogLevel, AizyBot

__version__ = "0.5.0"
__all__ = [
    "AizyBot",
    "CandleData",
    "OrderManager",
    "OrderStatus",
    "Order",
    "TestEngine",
    "Trade",
    "WebSocketHandler",
    "TradingPair",
    "LogLevel"
] 