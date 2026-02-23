#!/bin/bash

# Trading Bot Setup Script
# This script helps you set up the Binance Futures Trading Bot

echo "================================================"
echo "Binance Futures Trading Bot - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)' 2>/dev/null; then
    echo "   ❌ Error: Python 3.8 or higher is required"
    exit 1
fi
echo "   ✅ Python version is compatible"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "   ✅ Dependencies installed successfully"
else
    echo "   ❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔐 Setting up environment variables..."
    echo "   Creating .env file from template..."
    cp .env.example .env
    echo "   ✅ .env file created"
    echo ""
    echo "   ⚠️  IMPORTANT: Edit .env file and add your Binance Futures Testnet API credentials"
    echo "   Get your credentials from: https://testnet.binancefuture.com"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory ready"
echo ""

# Test connection (optional)
echo "🧪 Would you like to test the connection now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Testing connection to Binance Futures Testnet..."
    python3 cli.py test
    echo ""
fi

echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API credentials"
echo "2. Run: python3 cli.py test"
echo "3. Try a test order: python3 cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001"
echo ""
echo "For help: python3 cli.py --help"
echo ""
