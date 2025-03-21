from datetime import datetime
import time
from utils import get_value
from data_fetcher import DataFetcher
from config import API_KEY, SECRET_KEY, LOG_LEVEL, INTERVAL
from logger import setup_logger
import logging

# Set up a logger for the API client
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger = setup_logger('DeltaExchangeAPIClient', log_file='delta.log', log_level=log_level)

def main():
    # Initialize DataFetcher with your API Key
    data_fetcher = DataFetcher(API_KEY, SECRET_KEY)

    ticker_list = ["ETHUSD", "BTCUSD"]
    while True:
        try:
            # Get live ticker data
            for ticker in ticker_list:
                ticker_data = data_fetcher.get_ticker_data(ticker)

                if ticker_data:
                    live_value = get_value(ticker_data["result"], "mark_price")
                    print(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, {ticker}, {live_value}")
                else:
                    print("Could not retrieve live data.")

            time.sleep(INTERVAL)
        except EOFError:
            print("\nCtrl+D pressed. Exiting the loop.")
            break 

if __name__ == "__main__":
    main()
