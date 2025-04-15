import os
import requests
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pathlib import Path

# --- Load environment variables from .env ---
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# --- API Keys ---
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
FINANCIAL_DATASETS_API_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# --- Confirm loaded keys ---
print("Alpha Vantage API Key:", ALPHA_API_KEY)
print("FinancialDatasets API Key:", FINANCIAL_DATASETS_API_KEY)
print("Polygon.io API Key:", POLYGON_API_KEY)

# --- Common date range: last 7 days ---
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
START_DATE = start_date.strftime('%Y-%m-%d')
END_DATE = end_date.strftime('%Y-%m-%d')

# --- Alpha Vantage ---
def fetch_alpha_vantage_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# --- Yahoo Finance ---
def fetch_yahoo_data(symbol, period="7d"):
    stock = yf.Ticker(symbol)
    return stock.history(period=period)

# --- FinancialDatasets.ai ---
def fetch_financialdatasets_data(symbol):
    url = f"https://api.financialdatasets.ai/prices/?ticker={symbol}&interval=day&interval_multiplier=1&start_date={START_DATE}&end_date={END_DATE}"
    headers = {"X-Api-Key": FINANCIAL_DATASETS_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# --- Polygon.io (new addition) ---
def fetch_polygon_daily_data(symbol):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{START_DATE}/{END_DATE}"
    params = {
        "apiKey": POLYGON_API_KEY,
        "adjusted": "true",
        "sort": "asc"
    }
    response = requests.get(url, params=params)
    return response.json()
