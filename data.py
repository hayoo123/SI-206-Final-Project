import requests
import yfinance as yf

# Alpha Vantage Setup
ALPHA_API_KEY = "your_api_key_here"
ALPHA_URL = "https://www.alphavantage.co/query"

def fetch_alpha_vantage_data(symbol):
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(ALPHA_URL, params=params)
    data = response.json()
    return data

# Yahoo Finance with yfinance
def fetch_yahoo_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="7d")  # past 7 days of daily data
    return hist


import os
from dotenv import load_dotenv
import requests

# Load the .env file
load_dotenv()

# Access your API key
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")

def fetch_alpha_vantage_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(base_url, params=params)
    return response.json()
