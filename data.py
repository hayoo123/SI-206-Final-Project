import os
import requests
import yfinance as yf
from dotenv import load_dotenv
import time

load_dotenv()

# Access and create the API keys from the .env file

ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
FINANCIALDATASETS_API_KEY = os.getenv("FINANCIALDATASETS_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Fetching Alpha Vantagr weekly data"
def fetch_alpha_vantage_data(symbol):
    """Fetch weekly time series data from Alpha Vantage."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# Yahoo Finance last 7 days
def fetch_yahoo_data(symbol, period="7d"):
    """Fetch historical stock data from Yahoo Finance."""
    stock = yf.Ticker(symbol)
    return stock.history(period=period)

# fin.io API (Finnhub) weekly candles
def fetch_finnhub_data(symbol):
    """Fetch weekly candle data from Finnhub API."""
    start_time = int(time.mktime(time.strptime('2017-01-01', '%Y-%m-%d')))
    end_time = int(time.time())
    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        'symbol': symbol,
        'resolution': 'W',
        'from': start_time,
        'to': end_time,
        'token': FINNHUB_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# FinancialDatasets.ai API
def fetch_financialdatasets_data(symbol, start_date="2020-01-01", end_date="2024-01-01"):
    """Fetch weekly stock prices from FinancialDatasets.ai."""
    url = f"https://api.financialdatasets.ai/prices/?ticker={symbol}&interval=week&interval_multiplier=1&start_date={start_date}&end_date={end_date}"
    headers = {
        "X-Api-Key": FINANCIALDATASETS_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

