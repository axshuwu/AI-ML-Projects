def validate_symbol(symbol: str) -> str:
    if not symbol.endswith("USDT"):
        raise ValueError("Only USDT-M symbols allowed (e.g., BTCUSDT)")
    return symbol.upper()


def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
    return quantity


def validate_price(price, order_type):
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price must be provided and > 0 for LIMIT orders")
    return price
