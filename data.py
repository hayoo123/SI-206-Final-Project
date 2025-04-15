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

# Print API keys to verify they are loaded correctly
print("Alpha Vantage API Key:", ALPHA_API_KEY)
print("FinancialDatasets API Key:", FINANCIAL_DATASETS_API_KEY)

# Common start and end dates for data retrieval (past two weeks)
end_date = datetime.now()
start_date = end_date - timedelta(days=14)
START_DATE = start_date.strftime('%Y-%m-%d')
END_DATE = end_date.strftime('%Y-%m-%d')

# Fetching Alpha Vantage daily data
def fetch_alpha_vantage_data(symbol):
    """Fetch daily time series data from Alpha Vantage for the past two weeks."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Alpha Vantage Response:", data)
    
    # Filter data to the past two weeks
    time_series = data.get("Time Series (Daily)", {})
    filtered_data = {date: metrics for date, metrics in time_series.items() if START_DATE <= date <= END_DATE}
    print(f"Filtered Alpha Vantage Data for {symbol}: {filtered_data}")
    
    return filtered_data

# Yahoo Finance last 14 days
def fetch_yahoo_data(symbol, period="14d"):
    """Fetch historical stock data from Yahoo Finance."""
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    print("Yahoo Finance Response:", data)
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
