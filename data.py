# data.py
import os
import requests
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# API Keys
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
FINANCIAL_DATASETS_API_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Common date range (7 days for default fetch)
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
START_DATE = start_date.strftime('%Y-%m-%d')
END_DATE = end_date.strftime('%Y-%m-%d')

print("Alpha Vantage API Key:", ALPHA_API_KEY)
print("FinancialDatasets API Key:", FINANCIAL_DATASETS_API_KEY)
print("Polygon.io API Key:", POLYGON_API_KEY)

# Alpha Vantage

def fetch_alpha_vantage_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# Yahoo Finance

def fetch_yahoo_data(symbol, period="7d"):
    stock = yf.Ticker(symbol)
    return stock.history(period=period)

# FinancialDatasets.ai

def fetch_financialdatasets_data(symbol, start_date, end_date):
    url = f"https://api.financialdatasets.ai/prices/?ticker={symbol}&interval=day&interval_multiplier=1&start_date={start_date}&end_date={end_date}"
    headers = {"X-Api-Key": FINANCIAL_DATASETS_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Polygon.io

def fetch_polygon_daily_data(symbol, start_date, end_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "apiKey": POLYGON_API_KEY,
        "adjusted": "true",
        "sort": "asc"
    }
    response = requests.get(url, params=params)
    return response.json()
