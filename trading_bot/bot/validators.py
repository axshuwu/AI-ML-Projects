"""
Input Validation Module
Validates user inputs for trading parameters
"""

from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class InputValidator:
    """
    Validates trading inputs to ensure they meet requirements
    before being sent to the API.
    """
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT']
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol format.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Uppercase symbol string
            
        Raises:
            ValidationError: If symbol is invalid
        """
        if not symbol:
            raise ValidationError("Symbol cannot be empty")
        
        symbol = symbol.upper().strip()
        
        # Basic format check - symbols should be alphanumeric
        if not symbol.isalnum():
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        # Common trading pairs end with USDT, BUSD, etc.
        if len(symbol) < 6:
            raise ValidationError(f"Symbol too short: {symbol}")
        
        logger.debug(f"Symbol validated: {symbol}")
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """
        Validate order side (BUY/SELL).
        
        Args:
            side: Order side
            
        Returns:
            Uppercase side string
            
        Raises:
            ValidationError: If side is invalid
        """
        if not side:
            raise ValidationError("Side cannot be empty")
        
        side = side.upper().strip()
        
        if side not in InputValidator.VALID_SIDES:
            raise ValidationError(
                f"Invalid side: {side}. Must be one of {InputValidator.VALID_SIDES}"
            )
        
        logger.debug(f"Side validated: {side}")
        return side
    
    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """
        Validate order type (MARKET/LIMIT).
        
        Args:
            order_type: Type of order
            
        Returns:
            Uppercase order type string
            
        Raises:
            ValidationError: If order type is invalid
        """
        if not order_type:
            raise ValidationError("Order type cannot be empty")
        
        order_type = order_type.upper().strip()
        
        if order_type not in InputValidator.VALID_ORDER_TYPES:
            raise ValidationError(
                f"Invalid order type: {order_type}. Must be one of {InputValidator.VALID_ORDER_TYPES}"
            )
        
        logger.debug(f"Order type validated: {order_type}")
        return order_type
    
    @staticmethod
    def validate_quantity(quantity: str) -> float:
        """
        Validate order quantity.
        
        Args:
            quantity: Order quantity as string
            
        Returns:
            Quantity as float
            
        Raises:
            ValidationError: If quantity is invalid
        """
        try:
            qty = float(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid quantity: {quantity}. Must be a number")
        
        if qty <= 0:
            raise ValidationError(f"Quantity must be positive: {qty}")
        
        logger.debug(f"Quantity validated: {qty}")
        return qty
    
    @staticmethod
    def validate_price(price: str, required: bool = True) -> float:
        """
        Validate order price.
        
        Args:
            price: Order price as string
            required: Whether price is required
            
        Returns:
            Price as float, or None if not required and not provided
            
        Raises:
            ValidationError: If price is invalid
        """
        if not price or price.strip() == '':
            if required:
                raise ValidationError("Price is required for LIMIT orders")
            return None
        
        try:
            prc = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid price: {price}. Must be a number")
        
        if prc <= 0:
            raise ValidationError(f"Price must be positive: {prc}")
        
        logger.debug(f"Price validated: {prc}")
        return prc
    
    @staticmethod
    def validate_all(
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str = None
    ) -> Tuple[str, str, str, float, float]:
        """
        Validate all order parameters at once.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Tuple of (symbol, side, order_type, quantity, price)
            
        Raises:
            ValidationError: If any parameter is invalid
        """
        logger.info("Validating order parameters...")
        
        # Validate each parameter
        validated_symbol = InputValidator.validate_symbol(symbol)
        validated_side = InputValidator.validate_side(side)
        validated_order_type = InputValidator.validate_order_type(order_type)
        validated_quantity = InputValidator.validate_quantity(quantity)
        
        # Price validation depends on order type
        price_required = validated_order_type == 'LIMIT'
        validated_price = InputValidator.validate_price(price, required=price_required)
        
        logger.info("All parameters validated successfully")
        
        return (
            validated_symbol,
            validated_side,
            validated_order_type,
            validated_quantity,
            validated_price
        )
