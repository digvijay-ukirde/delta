from datetime import datetime
import time
from utils import get_value
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
    while True:
        try:
            # Get live ticker data
            for product in PRODUCTS:
                # ticker_data = data_fetcher.get_tickers_data(product["symbol"])

                # if ticker_data:
                #     json_data = ticker_data["result"]
                #     mark_price = get_value(json_data, "mark_price")
                #     print(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, MarketPrice: {mark_price}")
                # else:
                #     print("Could not retrieve live data.")

                # Get live historical candle data
                current_time = int(time.time())
                start = current_time - (current_time % 300) 
                end = current_time
                params = {
                    "resolution": product["resolution"],
                    "symbol": product["symbol"],
                    "start": start,
                    "end": end
                }
                historical_data = data_fetcher.get_history_candles_data(params)

                if historical_data["result"]:
                    print(historical_data["result"])
                    json_data = historical_data["result"][0]
                    high = get_value(json_data, "high")
                    low = get_value(json_data, "low")
                    open = get_value(json_data, "open")
                    close = get_value(json_data, "close")
                    volume = get_value(json_data, "volume")
                    print(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, High: {high}, Low:{low}, Open: {open}, Close:{close}, Volume:{volume}")
                else:
                    print("Could not retrieve live data. Probably at the end of candle. Sleeping for a minute.")
                    time.sleep(60)

            time.sleep(INTERVAL)
        except EOFError:
            print("\nCtrl+D pressed. Exiting the loop.")
            break 

if __name__ == "__main__":
    main()
