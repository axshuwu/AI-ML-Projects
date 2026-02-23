import streamlit as st
from bot.client import BinanceFuturesClient
from bot.orders import create_order_payload
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logging

# Setup logging
logger = setup_logging()

st.set_page_config(
    page_title="Binance Futures Testnet Bot",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Binance Futures Testnet Trading Bot")
st.markdown("Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)")

# --- Sidebar ---
st.sidebar.header("Order Configuration")

symbol = st.sidebar.text_input("Symbol", value="BTCUSDT")
side = st.sidebar.selectbox("Side", ["BUY", "SELL"])
order_type = st.sidebar.selectbox("Order Type", ["MARKET", "LIMIT"])
quantity = st.sidebar.number_input("Quantity", min_value=0.0001, step=0.0001, value=0.001)

price = None
if order_type == "LIMIT":
    price = st.sidebar.number_input("Price", min_value=0.01, step=0.01)

place_order_btn = st.sidebar.button("🚀 Place Order")

# --- Main Logic ---
if place_order_btn:
    try:
        # Validate inputs
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(price, order_type)

        # Show request summary
        st.subheader("📋 Order Summary")
        st.write({
            "Symbol": symbol,
            "Side": side,
            "Order Type": order_type,
            "Quantity": quantity,
            "Price": price if order_type == "LIMIT" else "Market Price"
        })

        # Initialize client
        client = BinanceFuturesClient(logger)

        payload = create_order_payload(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        with st.spinner("Placing order..."):
            response = client.place_order(**payload)

        st.success("✅ Order Placed Successfully!")

        st.subheader("📦 Order Response")
        st.write({
            "Order ID": response.get("orderId"),
            "Status": response.get("status"),
            "Executed Quantity": response.get("executedQty"),
            "Average Price": response.get("avgPrice", "N/A"),
        })

    except Exception as e:
        st.error(f"❌ Order Failed: {str(e)}")
