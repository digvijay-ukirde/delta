from datetime import datetime, timezone, timedelta
import time
import math
from utils import get_value
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
        
    def format_tickers_data(self, product):
        ticker_data = self.get_tickers_data(product["symbol"])
        if ticker_data:
            json_data = ticker_data["result"]
            mark_price = get_value(json_data, "mark_price")
            logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, MarketPrice: {mark_price}")
        else:
            print("Could not retrieve live data.")
        return
        
    def format_historical_data(self, product, candle_count):
        time_units = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}
        # Get live historical candle data
        current_time = int(time.time())
        # Derive how much timespan is needed to get required candle count 
        diff = (min((int(product["resolution"][:-1])*candle_count+2), 2000) * time_units[product["resolution"][-1]])
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
        historical_data = self.get_history_candles_data(params)
        if historical_data["result"]:
            logger.debug(historical_data["result"])
            json_data = historical_data["result"]
            for index, candle in enumerate(json_data[:candle_count]):
                high = get_value(json_data[index], "high")
                low = get_value(json_data[index], "low")
                open = get_value(json_data[index], "open")
                close = get_value(json_data[index], "close")
                volume = get_value(json_data[index], "volume")
                logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, Candle: {index + 1}, High: {high}, Low:{low}, Open: {open}, Close:{close}, Volume:{volume}")
        else:
            print("Could not retrieve live data. Probably at the end of candle. Sleeping for a minute.")
            time.sleep(60)
        return json_data
    

    def format_live_threshold_movement(self, product, candle_count):
            lettest_candle = self.format_historical_data(product, candle_count)[0]
            change_diff = lettest_candle["high"] - lettest_candle["low"]
            logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, Change: {change_diff}")
            if change_diff > product["change"]:
                print(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, High: {lettest_candle["high"]}, Low: {lettest_candle["high"]}, Change: {change_diff}")     


    def execute_long_order(self, historical_candles, buy, sell, profit):
        pl = 0
        for index, candle in enumerate(historical_candles):
            # if it breacks resistanace or support
            high = get_value(historical_candles[index], "high")
            low = get_value(historical_candles[index], "low")
            if high >= (buy+profit): 
                print(f"Profit achieved, Selling the asset. Sell: {buy+profit}")
                pl = profit
                break
            elif low <= sell:
                print(f"Loss booked, Selling the asset. Sell: {sell}")
                pl = (sell-buy)
                break        
        return pl
    
    def execute_short_order(self, historical_candles, sell, buy, profit):
        pl = 0
        for index, candle in enumerate(historical_candles):
            # if it breacks resistanace or support
            high = get_value(historical_candles[index], "high")
            low = get_value(historical_candles[index], "low")
            if low <= sell-profit: 
                print(f"Profit achieved, Buying the asset. Buy: {sell-profit}")
                pl = profit
                break
            elif high >= buy:
                print(f"Loss booked, Buying the asset. Buy: {buy}")
                pl = (sell-buy)
                break        
        return pl

    def check_order_fessibility(self, historical_candles, resistance, support, profit):
        buy = 0
        sell = 0
        pl = 0
        for index, candle in enumerate(historical_candles):
            # if it breacks resistanace or support
            high = get_value(historical_candles[index], "high")
            low = get_value(historical_candles[index], "low")
            if high >= resistance: 
                buy = resistance
                target = resistance + profit
                sell = support 
                print(f"Broke Resistance, Buying the asset. Buy: {buy}, Set Profit Taregt: {target}, Set SL: {sell}")
                pl = pl + self.execute_long_order(historical_candles, buy, sell, profit)
                break
            elif low <= support:
                sell = support
                target = support - profit
                buy = resistance
                print(f"Broke Support, Selling the asset. Sell: {sell}, Set Profit Taregt: {target}, Set SL: {buy}")
                pl = pl + self.execute_short_order(historical_candles, sell, buy, profit)
                break
        return pl


    def backtrack_historical_threshold_logic(self, product, candle_count):
            pl = 0
            ist = timezone(timedelta(hours=5, minutes=30))
            historical_candles = self.format_historical_data(product, candle_count)[::-1]
            for index, candle in enumerate(historical_candles):
                std_time = datetime.fromtimestamp(get_value(historical_candles[index], "time"), tz=ist)
                time = std_time.strftime('%Y:%m:%d:%H:%M')
                high = get_value(historical_candles[index], "high")
                low = get_value(historical_candles[index], "low")
                open = get_value(historical_candles[index], "open")
                close = get_value(historical_candles[index], "close")
                volume = get_value(historical_candles[index], "volume")
                logger.debug(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, Candle: {index + 1}, Time: {time}, High: {high}, Low:{low}, Open: {open}, Close:{close}, Volume:{volume}")

                change_diff = high - low
                if change_diff > product["change"]:
                    resistance = math.ceil(high)
                    support = math.floor(low)
                    #print(f"{datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}, Product: {product["name"]}, Candle: {index + 1}, Time: {time}, Resistance: {resistance}, Support: {support}, Change: {change_diff}")
                    pl = pl + (self.check_order_fessibility(historical_candles[index:], resistance, support, product["profit"]))
                    print(pl)



                
                

