import logging
from enum import Enum
from typing import Optional, Any, Callable, Awaitable, List, Union
from .CandleData import CandleData
from .OrderManager import OrderManager, OrderStatus
from .Trade import Trade
from .WebSocketHandler import WebSocketHandler

class TradingPair(Enum):
    BTCUSD = "BTC/USD"
    ETHUSD = "ETH/USD"
    SOLUSD = "SOL/USD"

class LogLevel(Enum):
    INFO = "info"
    DEBUG = "debug"
    ERROR = "error"

class AizyBot:
    """Base trading bot class implementing core trading functionality."""
    
    def __init__(self, log_file: str = "log.txt", websocket: Optional[Any] = None) -> None:
        self.logger: logging.Logger = self._setup_logger(log_file)
        self.websocket_handler: WebSocketHandler = WebSocketHandler(self.logger)
        self.order_manager: OrderManager = OrderManager(self.logger)
        self.websocket_handler.set_websocket(websocket)
        self.websocket_handler.set_callback(self.middleware)
        self.current_price: float = None

    async def middleware(self, candle_data: CandleData) -> None:
        """Middleware for processing candle data."""
        self.current_price = candle_data.close
        await self.bot_action(candle_data)

    async def bot_setup(self) -> None:
        """Initialize bot settings and configurations."""
        raise NotImplementedError("bot_setup method should be implemented by the subclass")

    async def bot_action(self, candle_data: CandleData) -> None:
        """Process incoming candle data and execute trading strategy.
        
        Args:
            candle_data: Candlestick data for analysis
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("bot_action method should be implemented by the subclass")

    async def log_event(self, event: str, level: int = logging.INFO) -> None:
        """Log an event.
        
        Args:
            event: The event to log
        """
        self.logger.log(level, event)

    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Configure logging for the bot.
        
        Args:
            log_file: Path to the log file
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger("AizyBot")
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        return logger

    async def get_kline(self, exchange: str, crypto: str, interval: str = "1m"):
        """
        Subscribe to a stream of klines.
        
        Args:
            exchange (str): The exchange to subscribe to (e.g., 'binance')
            crypto (str): The cryptocurrency pair to subscribe to (e.g., 'BTCUSDT')
            interval (str): The kline interval (default: '1m'). Options: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
        
        Raises:
            ValueError: If the interval is not one of the valid options
        """
        valid_intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        if interval not in valid_intervals:
            raise ValueError(f"Invalid interval: {interval}. Must be one of: {', '.join(valid_intervals)}")
        self.logger.info(f"Getting kline data for {exchange} {crypto} {interval}\nNote: This is a placeholder and will be implemented in production.")
        
    async def start(self) -> None:
        """Start the bot and establish WebSocket connection."""
        await self.websocket_handler.connect()
        self.logger.info("Bot started and listening for messages.")

    async def place_market_order(self, side: str, size: float, pair: TradingPair, take_profit: float = None, stop_loss: float = None, leverage: float = 1) -> None:
        """Place a new trading order.
        
        Args:
            side: Order side ('buy' or 'sell')
            amount: Order quantity
            price: Order price
            pair: TradingPair enum
            order_type: Type of order (default: 'market')
        """
        if not isinstance(pair, TradingPair):
            raise ValueError("pair must be a TradingPair enum")
        
        price = self.current_price
        order = self.order_manager.create_order(side, size, price, pair, take_profit, stop_loss, leverage)
        
        if self.order_manager.validate_order(order):
            self.order_manager.execute_order(order)
            if self.websocket_handler.ws:
                await self.websocket_handler.ws.send_order(order)

    async def close_trade(self, order: Union[str, Trade]) -> None:
        """Close an active trade.
        
        Args:
            order: Either the order ID (str) or Trade object to close
        """
        if isinstance(order, str):
            order = next((o for o in self.order_manager.orders if o.order_id == order), None)
        
        if order and order.status == OrderStatus.ACTIVE or order.status == OrderStatus.VALIDATED:
            self.order_manager.close_order(order)
            if self.websocket_handler.ws:
                await self.websocket_handler.ws.send_close_order(order)

    def list_active_trades(self) -> List[Trade]:
        """Get all active trades.
        
        Returns:
            List of active Trade objects
        """
        return self.order_manager.list_active_trades()

    def list_pending_orders(self) -> List[Trade]:
        """Get all pending orders.
        
        Returns:
            List of pending Trade objects
        """
        return self.order_manager.list_pending_orders()
