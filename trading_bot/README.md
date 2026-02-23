Binance Futures Trading Bot 🤖

A clean, professional Python trading bot for Binance Futures Testnet (USDT-M). This application provides a robust command-line interface for placing MARKET and LIMIT orders with proper validation, error handling, and logging.

Features

- ✅ **Order Types**: Support for MARKET and LIMIT orders
- ✅ **Order Sides**: Both BUY and SELL operations
- ✅ **Input Validation**: Comprehensive validation of all trading parameters
- ✅ **Error Handling**: Graceful handling of API, network, and validation errors
- ✅ **Structured Logging**: Detailed logs for debugging and audit trails
- ✅ **Clean CLI**: User-friendly command-line interface with Click
- ✅ **Modular Design**: Separated concerns (client, orders, validators, CLI)
- ✅ **Type Safety**: Type hints throughout the codebase


Setup Instructions

 1. Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- API credentials from Binance Futures Testnet

 2. Get API Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register or log in to your account
3. Navigate to API Management
4. Create a new API key
5. Save your API Key and API Secret securely

 3. Install Dependencies

```bash
# Clone or download this repository
cd trading_bot

# Install required packages
pip install -r requirements.txt
```

 4. Configure API Credentials

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_api_secret_here
```

**Important**: Never commit your `.env` file to version control!

 5. Test Connection

```bash
python cli.py test
```

You should see:
```
✅ Connection successful!
   The bot can communicate with Binance Futures Testnet API
```

Usage

 Basic Command Structure

```bash
python cli.py order [OPTIONS]
```

 Required Options

- `--symbol, -s`: Trading pair (e.g., BTCUSDT, ETHUSDT)
- `--side, -d`: Order side (BUY or SELL)
- `--type, -t`: Order type (MARKET or LIMIT)
- `--quantity, -q`: Order quantity

 Optional Options

- `--price, -p`: Order price (required for LIMIT orders)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

Examples

Example 1: Market Buy Order

```bash
python cli.py order \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

**Expected Output:**
```
🔄 Initializing connection to Binance Futures Testnet...
✅ Connected successfully

📋 Order Summary:
   Symbol:       BTCUSDT
   Side:         BUY
   Type:         MARKET
   Quantity:     0.001
   Price:        MARKET (best available)

🚀 Placing order...

============================================================
ORDER RESPONSE
============================================================
Order ID:         12345678
Client Order ID:  web_abc123def456
Symbol:           BTCUSDT
Status:           FILLED
Side:             BUY
Type:             MARKET
Quantity:         0.001
Executed Qty:     0.001
Average Price:    45000.50
Update Time:      1234567890123
============================================================

✅ Order placed successfully!

📝 Full details logged to: logs/trading_bot_20240215_143022.log
```

Example 2: Limit Sell Order

```bash
python cli.py order \
  --symbol ETHUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.01 \
  --price 2500
```

**Expected Output:**
```
🔄 Initializing connection to Binance Futures Testnet...
✅ Connected successfully

📋 Order Summary:
   Symbol:       ETHUSDT
   Side:         SELL
   Type:         LIMIT
   Quantity:     0.01
   Price:        2500

🚀 Placing order...

============================================================
ORDER RESPONSE
============================================================
Order ID:         87654321
Client Order ID:  web_xyz789abc123
Symbol:           ETHUSDT
Status:           NEW
Side:             SELL
Type:             LIMIT
Quantity:         0.01
Executed Qty:     0.000
Price:            2500.0
Update Time:      1234567890456
============================================================

✅ Order placed successfully!

📝 Full details logged to: logs/trading_bot_20240215_143522.log
```

Example 3: View Account Information

```bash
python cli.py account
```

Example 4: Debug Mode

For detailed debugging information:

```bash
python cli.py --log-level DEBUG order \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

Understanding Log Files

Each time you run the bot, a new log file is created in the `logs/` directory with a timestamp:

```
logs/trading_bot_20240215_143022.log
```

**Log File Contents:**
- API request details
- Request/response timestamps
- Order parameters
- Validation results
- Success/error messages
- Full API responses

**Example Log Entries:**

```
2024-02-15 14:30:22 - bot.logging_config - INFO - Logging initialized
2024-02-15 14:30:22 - bot.client - INFO - Binance Futures Client initialized
2024-02-15 14:30:23 - bot.orders - INFO - Initiating order placement: MARKET BUY 0.001 BTCUSDT
2024-02-15 14:30:23 - bot.validators - INFO - Validating order parameters...
2024-02-15 14:30:23 - bot.validators - INFO - All parameters validated successfully
2024-02-15 14:30:23 - bot.orders - INFO - ============================================================
2024-02-15 14:30:23 - bot.orders - INFO - ORDER REQUEST SUMMARY
2024-02-15 14:30:23 - bot.orders - INFO - ============================================================
2024-02-15 14:30:23 - bot.orders - INFO - Symbol:       BTCUSDT
2024-02-15 14:30:23 - bot.orders - INFO - Side:         BUY
2024-02-15 14:30:23 - bot.orders - INFO - Type:         MARKET
2024-02-15 14:30:23 - bot.orders - INFO - Quantity:     0.001
2024-02-15 14:30:23 - bot.orders - INFO - Price:        MARKET (best available)
2024-02-15 14:30:23 - bot.orders - INFO - ============================================================
2024-02-15 14:30:23 - bot.client - INFO - Placing MARKET BUY order for 0.001 BTCUSDT
2024-02-15 14:30:23 - bot.client - INFO - Making POST request to /fapi/v1/order
2024-02-15 14:30:24 - bot.client - INFO - Request to /fapi/v1/order successful
2024-02-15 14:30:24 - bot.orders - INFO - Order placed successfully. Order ID: 12345678
```

Error Handling

The bot handles various error scenarios gracefully:

1. Validation Errors

```bash
python cli.py order --symbol BTC --side BUY --type MARKET --quantity 0.001
```

Output:
```
❌ Validation Error: Symbol too short: BTC
```

2. Missing Price for Limit Orders

```bash
python cli.py order --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
```

Output:
```
❌ Validation Error: Price is required for LIMIT orders
```

3. API Errors

If the API returns an error (e.g., insufficient balance):
```
❌ API Error -2019: Margin is insufficient
```

4. Network Errors

If there's a connection issue:
```
❌ Unexpected Error: Connection timeout
```

Advanced Usage

Custom Log Level

```bash
python cli.py --log-level DEBUG order \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001
```

Help Command

```bash
python cli.py --help
python cli.py order --help
```

Best Practices

1. **Never commit your `.env` file** - It contains sensitive API credentials
2. **Start with small quantities** - Test with minimal amounts first
3. **Check logs** - Review log files after each order for debugging
4. **Use testnet** - Always use testnet for development and testing
5. **Validate inputs** - The bot validates inputs, but double-check your commands

Assumptions

- API credentials are valid and have trading permissions
- The Binance Futures Testnet is accessible
- Python 3.8+ is installed
- Trading pairs (symbols) exist and are active on the testnet
- User has basic command-line knowledge

Troubleshooting

 Issue: "API credentials not found"

**Solution**: Ensure your `.env` file exists and contains valid credentials.

```bash
# Check if .env exists
ls -la .env

# Verify contents (without revealing secrets)
cat .env
```

Issue: "Connection failed"

**Solution**: 
1. Check your internet connection
2. Verify testnet URL is accessible: https://testnet.binancefuture.com
3. Ensure API key is valid

Issue: "Invalid symbol"

**Solution**: Use valid trading pairs like:
- BTCUSDT
- ETHUSDT
- BNBUSDT
- Check [Binance Futures Testnet](https://testnet.binancefuture.com) for available pairs

Testing Checklist

Before submitting, ensure you've tested:

- ✅ MARKET BUY order
- ✅ MARKET SELL order
- ✅ LIMIT BUY order
- ✅ LIMIT SELL order
- ✅ Invalid input handling
- ✅ Log file generation
- ✅ Connection test

License

This project is for educational purposes as part of a job application task.

---

**Note**: This bot is designed for the Binance Futures Testnet only. Do not use production API credentials.
