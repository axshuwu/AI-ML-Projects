import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

load_dotenv()

class BinanceFuturesClient:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise EnvironmentError("API credentials not found in .env file")

        self.client = Client(self.api_key, self.api_secret)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def place_order(self, **kwargs):
        try:
            self.logger.info(f"Sending order request: {kwargs}")
            response = self.client.futures_create_order(**kwargs)
            self.logger.info(f"Order response: {response}")
            return response

        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e}")
            raise

        except BinanceRequestException as e:
            self.logger.error(f"Network error: {e}")
            raise

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

