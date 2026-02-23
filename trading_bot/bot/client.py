"""
Binance Futures Testnet Client
Handles API authentication and communication with Binance Futures Testnet
"""

import time
import hmac
import hashlib
import requests
from typing import Dict, Optional
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """
    A clean wrapper around the Binance Futures Testnet API.
    Handles authentication, request signing, and API communication.
    """
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Binance Futures client.
        
        Args:
            api_key: Your Binance Futures Testnet API key
            api_secret: Your Binance Futures Testnet API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        logger.info("Binance Futures Client initialized")
    
    def _generate_signature(self, params: Dict) -> str:
        """
        Generate HMAC SHA256 signature for API requests.
        
        Args:
            params: Dictionary of request parameters
            
        Returns:
            Hexadecimal signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = True) -> Dict:
        """
        Make a request to the Binance Futures API.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path
            params: Request parameters
            signed: Whether the request needs to be signed
            
        Returns:
            JSON response from the API
            
        Raises:
            requests.exceptions.RequestException: On network errors
            ValueError: On API errors
        """
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        
        if signed:
            # Add timestamp to params
            params['timestamp'] = int(time.time() * 1000)
            # Generate and add signature
            params['signature'] = self._generate_signature(params)
        
        logger.info(f"Making {method} request to {endpoint}")
        logger.debug(f"Request params: {params}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, params=params)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Log response
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Check for API-level errors
            if 'code' in data and 'msg' in data:
                error_msg = f"API Error {data['code']}: {data['msg']}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            logger.info(f"Request to {endpoint} successful")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"API error: {str(e)}")
            raise
    
    def test_connectivity(self) -> bool:
        """
        Test connectivity to the Binance Futures API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self._request('GET', '/fapi/v1/ping', signed=False)
            logger.info("Connectivity test successful")
            return True
        except Exception as e:
            logger.error(f"Connectivity test failed: {str(e)}")
            return False
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict:
        """
        Get exchange trading rules and symbol information.
        
        Args:
            symbol: Optional specific symbol to query
            
        Returns:
            Exchange information
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        return self._request('GET', '/fapi/v1/exchangeInfo', params=params, signed=False)
    
    def get_account_info(self) -> Dict:
        """
        Get current account information including balances.
        
        Returns:
            Account information
        """
        return self._request('GET', '/fapi/v2/account')
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = 'GTC'
    ) -> Dict:
        """
        Place an order on Binance Futures.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            order_type: Order type ('MARKET' or 'LIMIT')
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force for LIMIT orders (default: 'GTC')
            
        Returns:
            Order response from the API
            
        Raises:
            ValueError: On invalid parameters
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
        
        return self._request('POST', '/fapi/v1/order', params=params)
    
    def get_order(self, symbol: str, order_id: int) -> Dict:
        """
        Query order status.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to query
            
        Returns:
            Order information
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        return self._request('GET', '/fapi/v1/order', params=params)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an active order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Cancelling order {order_id} for {symbol}")
        
        return self._request('DELETE', '/fapi/v1/order', params=params)
