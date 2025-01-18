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

# Check if the API Key was loaded correctly
if not API_KEY:
    print("Error: API key not found. Please check your .env file.")
else:
    print("API Key loaded successfully.")

# AirNow API URL for real-time air quality data
API_URL = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={LATITUDE}&longitude={LONGITUDE}&distance=25&API_KEY={API_KEY}"


# Load datasets
def load_datasets():
    df1 = pd.read_csv("data/clean/kaggle_dataset1.csv")
    df2 = pd.read_csv("data/clean/opendata_dataset2.csv")
    return pd.concat([df1, df2], ignore_index=True)

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

# Combine data
def merge_data():
    # Load datasets and fetch API data
    dataset = load_datasets()
    api_data = fetch_api_data()
    if api_data is not None:
        dataset = pd.concat([dataset, api_data], ignore_index=True)
    return dataset

if __name__ == "__main__":
    df = merge_data()
    if df is not None:
        print(df.head())
        df.to_csv("data/merged_data.csv", index=False)
    else:
        print("No data fetched.")