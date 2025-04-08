import os
import requests
import yfinance as yf
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# Access the API key from the .env file
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
ALPHA_URL = "https://www.alphavantage.co/query"


# Alpha Vantage weekly data
def fetch_alpha_vantage_data(symbol):
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(ALPHA_URL, params=params)
    return response.json()

# Yahoo Finance last 7 days
def fetch_yahoo_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="7d")
    return hist


################# test ##################
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("ALPHA_API_KEY")
print("API Key:", api_key)

url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_WEEKLY",
    "symbol": "AAPL",
    "apikey": api_key
}

response = requests.get(url, params=params)
print("Status Code:", response.status_code)
print("Response:", response.json())

