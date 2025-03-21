
import requests
import time
import hmac
import hashlib
from config import API_URL, API_KEY, SECRET_KEY, LOG_LEVEL
from logger import setup_logger
import logging

# Set up a logger for the API client
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logger = setup_logger('DeltaExchangeAPIClient', log_file='delta.log', log_level=log_level)


class DeltaExchangeAPIClient:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = API_URL

    def _generate_signature(self, params):
        """Generate the HMAC SHA256 signature for authentication."""
        # Ensure we are using the sorted params to build the message
        params_string = '&'.join(f"{key}={value}" for key, value in sorted(params.items()))
        message = f"api_key={self.api_key}&{params_string}"
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        logger.debug(f"Generated signature: {signature}")
        
        # Generate the HMAC-SHA256 signature using the secret key
        return signature

    def get(self, endpoint, params=None):
        """Send GET request to the API."""
        url = f"{self.base_url}/{endpoint}"
        if not params:
            params = {}

        # Add API key and timestamp to params
        timestamp = str(int(time.time() * 1000))  # Timestamp in milliseconds
        params['api_key'] = self.api_key
        params['timestamp'] = timestamp

        # Generate signature
        signature = self._generate_signature(params)
        params['signature'] = signature

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            logger.info(f"Sending GET request to {url} with params: {params} and headers: {headers}")
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            logger.info("Request successful.")
            return response.json()  # Return the response in JSON format
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")
            return None
