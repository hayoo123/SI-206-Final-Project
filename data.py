import os
import requests
import yfinance as yf
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

# Load environment variables from .env
load_dotenv()

# Access the API key from the .env file
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
FINANCIAL_DATASETS_API_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# Print API keys to verify they are loaded correctly
print("Alpha Vantage API Key:", ALPHA_API_KEY)
print("FinancialDatasets API Key:", FINANCIAL_DATASETS_API_KEY)
print("Finnhub API Key:", FINNHUB_API_KEY)

# Common start and end dates for data retrieval (past week)
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
START_DATE = start_date.strftime('%Y-%m-%d')
END_DATE = end_date.strftime('%Y-%m-%d')

# Fetching Alpha Vantage weekly data
def fetch_alpha_vantage_data(symbol, output_format="json"):
    """Fetch weekly time series data from Alpha Vantage."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Alpha Vantage Response:", data)
    return data

# Yahoo Finance last 7 days
def fetch_yahoo_data(symbol, period="7d"):
    """Fetch historical stock data from Yahoo Finance."""
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    print("Yahoo Finance Response:", data)
    return data

# Finnhub API weekly candles
def fetch_finnhub_data(symbol):
    """Fetch weekly candle data from Finnhub API."""
    start_time = int(time.mktime(start_date.timetuple()))
    end_time = int(time.mktime(end_date.timetuple()))
    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        'symbol': symbol,
        'resolution': 'D',  # Daily resolution to cover past week
        'from': start_time,
        'to': end_time,
        'token': FINNHUB_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Finnhub Response:", data)
    return data

# FinancialDatasets.ai API
def fetch_financialdatasets_data(symbol):
    """Fetch daily stock prices from FinancialDatasets.ai."""
    url = f"https://api.financialdatasets.ai/prices/?ticker={symbol}&interval=day&interval_multiplier=1&start_date={START_DATE}&end_date={END_DATE}"
    headers = {
        "X-Api-Key": FINANCIAL_DATASETS_API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print("FinancialDatasets Response:", data)
    return data
