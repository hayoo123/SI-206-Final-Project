# data_utils.py
import os
import requests
import sqlite3
from dotenv import load_dotenv

load_dotenv()
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
ALPHA_URL = "https://www.alphavantage.co/query"


def fetch_alpha_vantage_data(symbol):
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": ALPHA_API_KEY
    }
    response = requests.get(ALPHA_URL, params=params)
    return response.json()


def create_tables():
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY, 
            symbol TEXT UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weekly_data (
            stock_id INTEGER,
            date TEXT,
            open REAL,
            close REAL,
            high REAL,
            low REAL,
            volume INTEGER,
            UNIQUE(stock_id, date)
        )
    """)
    conn.commit()
    conn.close()


def insert_data(symbol):
    create_tables()
    data = fetch_alpha_vantage_data(symbol)
    time_series = data.get("Weekly Time Series", {})

    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

    count = 0
    for date, metrics in sorted(time_series.items(), reverse=True)[:25]:
        try:
            cur.execute('''
                INSERT OR IGNORE INTO weekly_data 
                (stock_id, date, open, close, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                stock_id,
                date,
                float(metrics["1. open"]),
                float(metrics["4. close"]),
                float(metrics["2. high"]),
                float(metrics["3. low"]),
                int(metrics["5. volume"])
            ))
            count += 1
        except Exception as e:
            print(f"Error inserting {date}: {e}")

    conn.commit()
    conn.close()
    print(f"Inserted {count} new rows for {symbol}")


# visualization_utils.py
import sqlite3
import matplotlib.pyplot as plt

def plot_stock_data(symbol, price_type):
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

    if price_type == "high_low_avg":
        cur.execute('''
            SELECT date, high, low FROM weekly_data
            WHERE stock_id = ?
            ORDER BY date ASC
            LIMIT 25
        ''', (stock_id,))
        rows = cur.fetchall()
        values = [(float(row[1]) + float(row[2])) / 2 for row in rows]
        ylabel = "High-Low Avg Price ($)"
        title = f"{symbol} Weekly High-Low Average Prices"

    else:
        cur.execute(f'''
            SELECT date, {price_type} FROM weekly_data
            WHERE stock_id = ?
            ORDER BY date ASC
            LIMIT 25
        ''', (stock_id,))
        rows = cur.fetchall()
        values = [float(row[1]) for row in rows]
        ylabel = f"{price_type.capitalize()} Price ($)"
        title = f"{symbol} Weekly {price_type.capitalize()} Prices"

    dates = [row[0] for row in rows]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o', linestyle='-', color='blue')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    conn.close()


# main.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from data_utils import insert_data
from visualization_utils import plot_stock_data

if __name__ == "__main__":
    symbol = "AAPL"
    insert_data(symbol)
    plot_stock_data(symbol, "close")
    plot_stock_data(symbol, "open")
    plot_stock_data(symbol, "high_low_avg")
