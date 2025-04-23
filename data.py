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

# Common date range
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
START_DATE = start_date.strftime('%Y-%m-%d')
END_DATE = end_date.strftime('%Y-%m-%d')

#### FETCHING DATA FROM EACH API: ####

# Alpha Vantage
def fetch_alpha_vantage_data(symbol):
    """
    Fetches weekly stock data for a given symbol using the Alpha Vantage API.

    Parameters:
    symbol (str): The stock ticker symbol (e.g., "AAPL").

    What the code does:
    - Constructs an API request using the symbol and Alpha Vantage key.
    - Sends a GET request to retrieve weekly stock data.
    - Parses and returns the response in JSON format.

    Returns:
    dict: A JSON object containing weekly stock data including open, high, low, close, and volume.
    """
    
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
    """
    Retrieves recent historical stock data using Yahoo Finance.

    Parameters:
    symbol (str): The stock ticker symbol.
    period (str, optional): The time period to retrieve (e.g., "7d", "1mo"). Default is "7d".

    What the code does:
    - Initializes a Ticker object using yfinance.
    - Requests historical data for the given symbol and period.
    - Returns the data as a Pandas object.

    Returns:
    Pamdas object: A DataFrame with columns like Open, High, Low, Close, and Volume.
    """
    
    stock = yf.Ticker(symbol)
    return stock.history(period=period)

# FinancialDatasets.ai
def fetch_financialdatasets_data(symbol, start_date, end_date):
    """
    Fetches daily stock data from FinancialDatasets.ai for a given date range.

    Parameters:
    symbol (str): The stock ticker symbol.
    start_date (str): Start date in "YYYY-MM-DD" format.
    end_date (str): End date in "YYYY-MM-DD" format.

    What the code does:
    - Builds a request URL with query parameters.
    - Sends a GET request to the FinancialDatasets.ai API.
    - Parses and returns the response as JSON.

    Returns:
    Dict: A JSON object with daily prices including open, high, low, close, and timestamps.
    """
    
    url = f"https://api.financialdatasets.ai/prices/?ticker={symbol}&interval=day&interval_multiplier=1&start_date={start_date}&end_date={end_date}"
    headers = {"X-Api-Key": FINANCIAL_DATASETS_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Polygon.io
def fetch_polygon_daily_data(symbol, start_date, end_date):
    """
    Fetches daily price data from Polygon.io for the given symbol and date range.

    Parameters:
    symbol (str): The stock ticker symbol.
    start_date (str): Start date in "YYYY-MM-DD" format.
    end_date (str): End date in "YYYY-MM-DD" format.

    What the code does:
    - Constructs a GET request to the Polygon.io API.
    - Sends the request with parameters for date range and ticker.
    - Returns parsed response data in JSON format.

    Returns:
    dict: A JSON object with daily data including open, high, low, close, and volume.
    """
    
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "apiKey": POLYGON_API_KEY,
        "adjusted": "true",
        "sort": "asc"
    }
    response = requests.get(url, params=params)
    return response.json()
