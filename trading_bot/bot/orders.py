"""
Order Placement Module
Contains logic for placing and managing orders
"""

from typing import Dict, Optional
import logging
from .client import BinanceFuturesClient
from .validators import InputValidator, ValidationError

logger = logging.getLogger(__name__)


class OrderManager:
    """
    Handles order placement and management operations.
    Combines validation and API interaction.
    """
    
    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize the OrderManager.
        
        Args:
            client: Initialized BinanceFuturesClient instance
        """
        self.client = client
        self.validator = InputValidator()
        logger.info("OrderManager initialized")
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str = None
    ) -> Dict:
        """
        Validate and place an order.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            order_type: Order type ('MARKET' or 'LIMIT')
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            
        Returns:
            Order response from the API
            
        Raises:
            ValidationError: If parameters are invalid
            ValueError: If API returns an error
            requests.exceptions.RequestException: On network errors
        """
        logger.info(f"Initiating order placement: {order_type} {side} {quantity} {symbol}")
        
        # Validate all inputs
        try:
            validated_symbol, validated_side, validated_order_type, \
            validated_quantity, validated_price = self.validator.validate_all(
                symbol, side, order_type, quantity, price
            )
        except ValidationError as e:
            logger.error(f"Validation failed: {str(e)}")
            raise
        
        # Log order request summary
        self._log_order_summary(
            validated_symbol,
            validated_side,
            validated_order_type,
            validated_quantity,
            validated_price
        )
        
        # Place the order via API
        try:
            response = self.client.place_order(
                symbol=validated_symbol,
                side=validated_side,
                order_type=validated_order_type,
                quantity=validated_quantity,
                price=validated_price
            )
            
            logger.info(f"Order placed successfully. Order ID: {response.get('orderId')}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise
    
    def _log_order_summary(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float]
    ) -> None:
        """
        Log a summary of the order request.
        
        Args:
            symbol: Trading pair
            side: Order side
            order_type: Order type
            quantity: Order quantity
            price: Order price (if applicable)
        """
        logger.info("=" * 60)
        logger.info("ORDER REQUEST SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Symbol:       {symbol}")
        logger.info(f"Side:         {side}")
        logger.info(f"Type:         {order_type}")
        logger.info(f"Quantity:     {quantity}")
        if price:
            logger.info(f"Price:        {price}")
        else:
            logger.info(f"Price:        MARKET (best available)")
        logger.info("=" * 60)
    
    @staticmethod
    def format_order_response(response: Dict) -> str:
        """
        Format order response for display.
        
        Args:
            response: Order response from API
            
        Returns:
            Formatted string representation
        """
        lines = [
            "=" * 60,
            "ORDER RESPONSE",
            "=" * 60,
            f"Order ID:         {response.get('orderId', 'N/A')}",
            f"Client Order ID:  {response.get('clientOrderId', 'N/A')}",
            f"Symbol:           {response.get('symbol', 'N/A')}",
            f"Status:           {response.get('status', 'N/A')}",
            f"Side:             {response.get('side', 'N/A')}",
            f"Type:             {response.get('type', 'N/A')}",
            f"Quantity:         {response.get('origQty', 'N/A')}",
            f"Executed Qty:     {response.get('executedQty', 'N/A')}",
        ]
        
        # Add price information if available
        if 'price' in response and response['price'] != '0':
            lines.append(f"Price:            {response.get('price', 'N/A')}")
        
        if 'avgPrice' in response and response['avgPrice'] != '0':
            lines.append(f"Average Price:    {response.get('avgPrice', 'N/A')}")
        
        # Add timestamp
        if 'updateTime' in response:
            lines.append(f"Update Time:      {response.get('updateTime', 'N/A')}")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """
        Get the status of an existing order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to query
            
        Returns:
            Order information
        """
        logger.info(f"Querying order status for Order ID: {order_id}")
        
        try:
            response = self.client.get_order(symbol, order_id)
            logger.info(f"Order status retrieved successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to get order status: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an existing order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        logger.info(f"Cancelling order {order_id} for {symbol}")
        
        try:
            response = self.client.cancel_order(symbol, order_id)
            logger.info(f"Order cancelled successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to cancel order: {str(e)}")
            raise
