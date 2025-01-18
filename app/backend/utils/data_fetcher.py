# data_fetcher.py

import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# AirNow API URL for fetching current air quality data based on latitude and longitude
LATITUDE = 27.732864  # Latitude for Kathmandu
LONGITUDE = 85.24719  # Longitude for Kathmandu
API_KEY = os.getenv("AIRNOW_API_KEY")  # Ensure this key is in your .env file

# AirNow API URL for real-time air quality data
API_URL = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={LATITUDE}&longitude={LONGITUDE}&distance=25&API_KEY={API_KEY}"

# Fetch API data
def fetch_api_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):  # Handle JSON response with list format
                return pd.DataFrame(data)
        else:
            print(f"Error: Unable to fetch data from API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching data from API: {e}")
    return None

# Fetch live data, calling the fetch_api_data function directly
def fetch_live_data():
    return fetch_api_data()
