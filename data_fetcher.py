# data_fetcher.py
from api_client import DeltaExchangeAPIClient
from credentials import LOG_LEVEL
from logger import setup_logger
import logging

# Set up a logger for the API client
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger = setup_logger('DeltaExchangeAPIClient', log_file='delta.log', log_level=log_level)

class DataFetcher:
    def __init__(self):
        self.client = DeltaExchangeAPIClient()

    def get_tickers_data(self, ticker):
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

    def get_history_candles_data(self, params):
        """Fetch live ticker data from Delta Exchange."""
        endpoint = f"history/candles"
        logger.info(f"Fetching historical data for {params['symbol']}...")

        data = self.client.get(endpoint, params)
        if data:
            logger.info(f"Historical data for {params['symbol']}: {data}")
            return data
        else:
            logger.error(f"Failed to retrieve Historical data for {params['symbol']}.")
            return None