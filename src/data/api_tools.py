# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 15:06:43 2023

@author: Ryan Bolger
"""

import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import requests
import logging
import os


# Initiate logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Load credentials from a local .env file
load_dotenv("./.env/tfl_api.env")


# Define a TFL API class to connect to the API and format queries
class TfLApiClient:
    def __init__(self, app_key=None):
        self.base_url = "https://api.tfl.gov.uk/"

        if app_key is None:
            self.app_key = os.getenv("TFL_API_APP_KEY")

    def make_request(self, endpoint, params=None):
        """
        Make a request to the TfL API.

        :param endpoint: The API endpoint path (e.g., 'BikePoint').
        :param params: Optional parameters for the API request.
        :return: The JSON response from the API.
        """
        if params is None:
            params = dict()

        # Include API credentials in the parameters
        params["app_key"] = self.app_key

        # Construct the full URL
        url = f"{self.base_url}{endpoint}"

        # Ignore other parameters for the time being...

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                logging.info("API request successful")
                logging.info(f"Returned {len(data)} rows")
                return data
            else:
                logging.warning(f"Error: {response.status_code}")
        except Exception as e:
            logging.warning(f"Error: {e}")


def main(endpoint, filepath):
    """Get an API response and save the returned data"""

    api = TfLApiClient()
    response_df = api.make_request(endpoint)
    response_df.to_csv(filepath + "tfl_response.csv", index=None)


if __name__ == "__main__":
    endpoint = input("Endpoint eg. BikePoint, AirQuality...:")
    filepath = input("Location to save:")
    logging.info("Querying API")
    main(endpoint, filepath)
