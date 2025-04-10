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


################# api key data  ##################
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


######### sort data kinda ########
import requests

# example URL (you likely already have this set up correctly)
url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=AAPL&apikey=your_api_key"

# make the API call
response = requests.get(url)

# convert the response to a dictionary
json_data = response.json()

# extract the actual time series data
data = json_data['Weekly Time Series']

# now you can do something with 'data', like:
for date, metrics in data.items():
    print(f"{date}: {metrics}")
    
############### AAPL closing prices (visual) ##################

import sqlite3
from data import fetch_alpha_vantage_data
import matplotlib.pyplot as plt

def insert_alpha_data(symbol):
    data = fetch_alpha_vantage_data(symbol)
    time_series = data.get("Weekly Time Series", {})

    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    # Insert symbol into stocks table and get stock_id
    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

    count = 0
    for date, metrics in sorted(time_series.items(), reverse=True):
        if count >= 25:
            break

        try:
            open_price = float(metrics["1. open"])
            high = float(metrics["2. high"])
            low = float(metrics["3. low"])
            close = float(metrics["4. close"])
            volume = int(metrics["5. volume"])
        except Exception as e:
            print(f"Skipping {date} due to error: {e}")
            continue

        try:
            cur.execute('''
                INSERT OR IGNORE INTO weekly_data 
                (stock_id, date, open, close, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (stock_id, date, open_price, close, high, low, volume))
            count += 1
        except Exception as e:
            print(f"Error inserting {date}: {e}")

    conn.commit()

    # Now plot the data
    cur.execute('''
        SELECT date, close FROM weekly_data
        WHERE stock_id = ?
        ORDER BY date ASC
        LIMIT 25
    ''', (stock_id,))
    rows = cur.fetchall()

    dates = [row[0] for row in rows]
    closes = [row[1] for row in rows]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, closes, marker='o', linestyle='-', color='blue')
    plt.title(f"{symbol} Weekly Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    conn.close()
    print(f"Inserted {count} new rows and generated chart for {symbol}")

if __name__ == "__main__":
    insert_alpha_data("AAPL")
    
    
############# AAPL for opening prices (visual) ##########
############### AAPL opening prices (visual) ##################

import sqlite3
from data import fetch_alpha_vantage_data
import matplotlib.pyplot as plt

def insert_alpha_data(symbol):
    data = fetch_alpha_vantage_data(symbol)
    time_series = data.get("Weekly Time Series", {})

    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    # Insert symbol into stocks table and get stock_id
    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

    count = 0
    for date, metrics in sorted(time_series.items(), reverse=True):
        if count >= 25:
            break

        try:
            open_price = float(metrics["1. open"])
            high = float(metrics["2. high"])
            low = float(metrics["3. low"])
            close = float(metrics["4. close"])
            volume = int(metrics["5. volume"])
        except Exception as e:
            print(f"Skipping {date} due to error: {e}")
            continue

        try:
            cur.execute('''
                INSERT OR IGNORE INTO weekly_data 
                (stock_id, date, open, close, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (stock_id, date, open_price, close, high, low, volume))
            count += 1
        except Exception as e:
            print(f"Error inserting {date}: {e}")

    conn.commit()

    # Now plot the opening prices
    cur.execute('''
        SELECT date, open FROM weekly_data
        WHERE stock_id = ?
        ORDER BY date ASC
        LIMIT 25
    ''', (stock_id,))
    rows = cur.fetchall()

    dates = [row[0] for row in rows]
    opens = [row[1] for row in rows]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, opens, marker='o', linestyle='-', color='green')
    plt.title(f"{symbol} Weekly Opening Prices")
    plt.xlabel("Date")
    plt.ylabel("Opening Price ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    conn.close()
    print(f"Inserted {count} new rows and generated chart for {symbol}")

if __name__ == "__main__":
    insert_alpha_data("AAPL")




