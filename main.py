import time
from data_fetcher import DataFetcher
from credentials import LOG_LEVEL
from config import PRODUCTS, INTERVAL
from logger import setup_logger
import logging

# Set up a logger for the API client
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger = setup_logger('DeltaExchangeAPIClient', log_file='delta.log', log_level=log_level)

def main():
    # Initialize DataFetcher
    data_fetcher = DataFetcher()
    data_fetcher.backtrack_historical_threshold_logic(PRODUCTS[1], 2000)
    # while True:
    #     try:
    #         # Get live ticker data
    #         for product in PRODUCTS:
    #             # data_fetcher.format_tickers_data(product)
    #             # data_fetcher.format_historical_data(product, 2000)
    #             # data_fetcher.format_live_threshold_movement(product, 1)
    #             data_fetcher.format_historical_threshold_movement(product, 2000)
    #         time.sleep(INTERVAL)
    #     except EOFError:
    #         print("\nCtrl+D pressed. Exiting the loop.")
    #         break 

    

if __name__ == "__main__":
    main()
