# data_fetcher.py
from api_client import DeltaExchangeAPIClient
from credentials import API_URL, API_KEY, SECRET_KEY, LOG_LEVEL
from logger import setup_logger
import logging

# Set up a logger for the API client
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger = setup_logger('DeltaExchangeAPIClient', log_file='delta.log', log_level=log_level)

class DataFetcher:
    def __init__(self, api_key, secret_key):
        self.client = DeltaExchangeAPIClient(api_key, secret_key)

    def get_ticker_data(self, ticker):
        """Fetch live ticker data from Delta Exchange."""
        endpoint = f"tickers/{ticker}"
        logger.info(f"Fetching ticker data for {ticker}...")

        data = self.client.get(endpoint)
        if data:
            logger.info(f"Ticker data for {ticker}: {data}")
            return data
        else:
            logger.error(f"Failed to retrieve ticker data for {ticker}.")
            return None
