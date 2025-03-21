from credentials import LOG_LEVEL
from logger import setup_logger
import logging

# Set up a logger for the API client
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger = setup_logger('DeltaExchangeAPIClient', log_file='delta.log', log_level=log_level)

def get_value(json_data, key):
    logger.debug(f"Json data: {json_data}")
    logger.debug(f"Key: {key}")
    return (json_data[key])