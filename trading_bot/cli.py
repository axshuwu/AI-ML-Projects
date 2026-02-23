#!/usr/bin/env python3
"""
CLI Entry Point for Binance Futures Trading Bot
Provides a clean command-line interface for placing orders
"""

import sys
import os
import click
from pathlib import Path
from dotenv import load_dotenv

from bot import (
    BinanceFuturesClient,
    OrderManager,
    ValidationError,
    setup_logging,
    get_logger
)

# Load environment variables from .env file
load_dotenv()

# Initialize logger
logger = None


def initialize_client() -> BinanceFuturesClient:
    """
    Initialize the Binance Futures client with API credentials.
    
    Returns:
        Initialized BinanceFuturesClient
        
    Raises:
        click.ClickException: If API credentials are not found
    """
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        raise click.ClickException(
            "API credentials not found. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET environment variables or create a .env file."
        )
    
    return BinanceFuturesClient(api_key, api_secret)


@click.group(invoke_without_command=True)
@click.option('--log-level', default='INFO', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
              help='Set logging level')
@click.pass_context
def cli(ctx, log_level):
    """
    Binance Futures Trading Bot - Place orders on Binance Futures Testnet
    
    Examples:
    
        # Place a market buy order
        python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
        
        # Place a limit sell order
        python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2000
    """
    global logger
    
    # Setup logging
    log_file = setup_logging(log_level=log_level)
    logger = get_logger(__name__)
    
    # Store log file in context for later use
    ctx.ensure_object(dict)
    ctx.obj['log_file'] = log_file
    
    # If no subcommand is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--symbol', '-s', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--side', '-d', required=True, 
              type=click.Choice(['BUY', 'SELL'], case_sensitive=False),
              help='Order side')
@click.option('--type', '-t', 'order_type', required=True,
              type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False),
              help='Order type')
@click.option('--quantity', '-q', required=True, help='Order quantity')
@click.option('--price', '-p', default=None, help='Order price (required for LIMIT orders)')
@click.pass_context
def order(ctx, symbol, side, order_type, quantity, price):
    """
    Place an order on Binance Futures Testnet.
    
    This command validates inputs, places the order, and displays the result.
    """
    logger.info("=" * 80)
    logger.info("STARTING ORDER PLACEMENT")
    logger.info("=" * 80)
    
    try:
        # Initialize client and order manager
        click.echo("🔄 Initializing connection to Binance Futures Testnet...")
        client = initialize_client()
        order_manager = OrderManager(client)
        
        # Test connectivity
        if not client.test_connectivity():
            raise click.ClickException("Failed to connect to Binance Futures Testnet")
        
        click.echo("✅ Connected successfully\n")
        
        # Display order summary
        click.echo("📋 Order Summary:")
        click.echo(f"   Symbol:       {symbol.upper()}")
        click.echo(f"   Side:         {side.upper()}")
        click.echo(f"   Type:         {order_type.upper()}")
        click.echo(f"   Quantity:     {quantity}")
        if price:
            click.echo(f"   Price:        {price}")
        else:
            click.echo(f"   Price:        MARKET (best available)")
        click.echo()
        
        # Place the order
        click.echo("🚀 Placing order...")
        response = order_manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Display formatted response
        click.echo()
        click.echo(OrderManager.format_order_response(response))
        
        # Success message
        status = response.get('status', 'UNKNOWN')
        if status in ['NEW', 'FILLED', 'PARTIALLY_FILLED']:
            click.echo()
            click.secho("✅ Order placed successfully!", fg='green', bold=True)
            logger.info("Order placement completed successfully")
        else:
            click.echo()
            click.secho(f"⚠️  Order status: {status}", fg='yellow', bold=True)
            logger.warning(f"Order placed with status: {status}")
        
        # Show log file location
        click.echo()
        click.echo(f"📝 Full details logged to: {ctx.obj['log_file']}")
        
    except ValidationError as e:
        click.secho(f"\n❌ Validation Error: {str(e)}", fg='red', bold=True)
        logger.error(f"Validation error: {str(e)}")
        sys.exit(1)
        
    except ValueError as e:
        click.secho(f"\n❌ API Error: {str(e)}", fg='red', bold=True)
        logger.error(f"API error: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        click.secho(f"\n❌ Unexpected Error: {str(e)}", fg='red', bold=True)
        logger.exception("Unexpected error occurred")
        sys.exit(1)


@cli.command()
def test():
    """
    Test connection to Binance Futures Testnet.
    """
    logger.info("Testing connection to Binance Futures Testnet...")
    
    try:
        click.echo("🔄 Testing connection to Binance Futures Testnet...")
        client = initialize_client()
        
        if client.test_connectivity():
            click.secho("✅ Connection successful!", fg='green', bold=True)
            click.echo("   The bot can communicate with Binance Futures Testnet API")
            logger.info("Connectivity test passed")
        else:
            click.secho("❌ Connection failed", fg='red', bold=True)
            logger.error("Connectivity test failed")
            sys.exit(1)
            
    except Exception as e:
        click.secho(f"❌ Error: {str(e)}", fg='red', bold=True)
        logger.exception("Connection test failed")
        sys.exit(1)


@cli.command()
@click.option('--symbol', '-s', help='Filter by specific symbol (optional)')
def account(symbol):
    """
    Display account information and balances.
    """
    try:
        click.echo("🔄 Fetching account information...")
        client = initialize_client()
        
        account_info = client.get_account_info()
        
        click.echo("\n" + "=" * 60)
        click.echo("ACCOUNT INFORMATION")
        click.echo("=" * 60)
        
        # Display balances
        if 'assets' in account_info:
            click.echo("\n💰 Balances:")
            for asset in account_info['assets']:
                balance = float(asset.get('walletBalance', 0))
                if balance > 0 or not symbol:
                    click.echo(f"   {asset['asset']:8s}: {balance:.8f}")
        
        # Display positions if any
        if 'positions' in account_info:
            click.echo("\n📊 Open Positions:")
            has_positions = False
            for position in account_info['positions']:
                pos_amt = float(position.get('positionAmt', 0))
                if pos_amt != 0:
                    has_positions = True
                    symbol_name = position['symbol']
                    if not symbol or symbol.upper() in symbol_name:
                        click.echo(f"   {symbol_name}: {pos_amt}")
            
            if not has_positions:
                click.echo("   No open positions")
        
        click.echo("=" * 60)
        logger.info("Account information retrieved successfully")
        
    except Exception as e:
        click.secho(f"\n❌ Error: {str(e)}", fg='red', bold=True)
        logger.exception("Failed to fetch account information")
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
