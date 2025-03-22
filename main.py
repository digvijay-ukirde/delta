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
    time_units = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}
    while True:
        try:
            # Get live ticker data
            for product in PRODUCTS:
                ticker_data = data_fetcher.get_tickers_data(product["symbol"])

                if ticker_data:
                    json_data = ticker_data["result"]
                    mark_price = get_value(json_data, "mark_price")
                    logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, MarketPrice: {mark_price}")
                else:
                    print("Could not retrieve live data.")

                # Get live historical candle data
                current_time = int(time.time())
                diff = (min((int(product["resolution"][:-1])*product["candles"]+2), 2000) * time_units[product["resolution"][-1]])
                logger.debug(f"Difference between start and end of time period of candles: {diff}")
                start = current_time - diff
                end = current_time
                params = {
                    "resolution": product["resolution"],
                    "symbol": product["symbol"],
                    "start": start,
                    "end": end
                }
                logger.debug(f"Params: ", params)
                historical_data = data_fetcher.get_history_candles_data(params)
                if historical_data["result"]:
                    logger.debug(historical_data["result"])
                    json_data = historical_data["result"]
                    for index, candle in enumerate(json_data[:product["candles"]]):
                        high = get_value(json_data[index], "high")
                        low = get_value(json_data[index], "low")
                        open = get_value(json_data[index], "open")
                        close = get_value(json_data[index], "close")
                        volume = get_value(json_data[index], "volume")
                        logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, Candle: {index}, High: {high}, Low:{low}, Open: {open}, Close:{close}, Volume:{volume}")

                    lettest_candle = json_data[0]
                    change_diff = lettest_candle["high"] - lettest_candle["low"]
                    logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, Change: {change_diff}")
                    if change_diff > product["change"]:
                        print(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, High: {lettest_candle["high"]}, Low: {lettest_candle["high"]}, Change: {change_diff}")     
                else:
                    print("Could not retrieve live data. Probably at the end of candle. Sleeping for a minute.")
                    time.sleep(60)

            time.sleep(INTERVAL)
        except EOFError:
            print("\nCtrl+D pressed. Exiting the loop.")
            break 

if __name__ == "__main__":
    main()
