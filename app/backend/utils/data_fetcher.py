import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# AirNow API URL for fetching current air quality data based on latitude and longitude
LATITUDE = 27.732864  # Latitude for Kathmandu
LONGITUDE = 85.24719  # Longitude for Kathmandu
API_KEY = os.getenv("AIRNOW_API_KEY")  # Ensure this key is in your .env file

# AirNow API URL for real-time air quality data
API_URLS = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={LATITUDE}&longitude={LONGITUDE}&distance=25&API_KEY={API_KEY}"


# Load datasets
def load_datasets():
    df = pd.read_csv("data/clean/weather_sorted_merged_data.csv")
    return df

# Fetch API data
def fetch_api_data():
    api_data = []
    for url in API_URLS:
        try:
            # Include the API key in the request URL for AirNow
            url_with_key = url + API_KEY
            response = requests.get(url_with_key)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):  # Handle JSON response with list format
                    api_data.append(pd.DataFrame(data))
            else:
                print(f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
    return pd.concat(api_data, ignore_index=True) if api_data else None
'''
# Combine data
def merge_data():
    # Load datasets and fetch API data
    dataset = load_datasets()
    api_data = fetch_api_data()
    if api_data is not None:
        dataset = pd.concat([dataset, api_data], ignore_index=True)
    return dataset
'''

if __name__ == "__main__":
    data = fetch_api_data()
    if data is not None:
        print("Data fetched from api successfully")
    else:
        print("No data fetched.")