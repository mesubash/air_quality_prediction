# Fetches data from APIs

import requests

API_URLS = [
    "https://api.openaq.org/v2/latest?city=Kathmandu",
    "https://api.waqi.info/feed/kathmandu/?token=235ec806411ead00b7b988c0ac56d1a23b1fd802"]

def fetch_live_data():
    aqi_data = {}
    for url in API_URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                aqi_data[url] = data
        except Exception as e:
            aqi_data[url] = {"error": str(e)}
    return aqi_data
