import sqlite3
from datetime import datetime
from data import fetch_alpha_vantage_data, fetch_yahoo_data, fetch_finnhub_data, fetch_financialdatasets_data
from db_setup import setup_database  # Import the setup_database function

def insert_alpha_vantage_data(symbol):
    data = fetch_alpha_vantage_data(symbol)
    time_series = data.get("Weekly Time Series", {})
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    
    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    stock_id = cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,)).fetchone()[0]
    
    count = 0
    for date, metrics in sorted(time_series.items(), reverse=True):
        if count >= 25:
            break
        try:
            cur.execute('''
            INSERT OR IGNORE INTO weekly_data 
            (stock_id, date, open, close, high, low, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_id, date,
                float(metrics["1. open"]),
                float(metrics["4. close"]),
                float(metrics["2. high"]),
                float(metrics["3. low"]),
                int(metrics["5. volume"])
            ))
            if cur.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"Error inserting {date}: {e}")
    
    cur.execute('''
    INSERT OR REPLACE INTO api_metadata 
    (stock_id, api_name, last_updated)
    VALUES (?, ?, ?)
    ''', (stock_id, "Alpha Vantage", datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"Inserted {count} new rows for {symbol} (Alpha Vantage).")

def insert_yahoo_data(symbol):
    data = fetch_yahoo_data(symbol, period="60d")
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    
    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    stock_id = cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,)).fetchone()[0]
    
    count = 0
    for index, row in data.iterrows():
        if count >= 25:
            break
        date = index.strftime("%Y-%m-%d")
        try:
            cur.execute('''
            INSERT OR IGNORE INTO weekly_data 
            (stock_id, date, open, close, high, low, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_id, date,
                row["Open"],
                row["Close"],
                row["High"],
                row["Low"],
                row["Volume"]
            ))
            if cur.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"Error inserting {date}: {e}")
    
    cur.execute('''
    INSERT OR REPLACE INTO api_metadata 
    (stock_id, api_name, last_updated)
    VALUES (?, ?, ?)
    ''', (stock_id, "Yahoo Finance", datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"Inserted {count} new rows for {symbol} (Yahoo Finance).")

def insert_finnhub_data(symbol):
    data = fetch_finnhub_data(symbol)
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    
    if 'error' in data:
        print(f"Finnhub API Error for {symbol}: {data['error']}")
        return
    
    required_keys = ['t', 'o', 'c', 'h', 'l', 'v']
    if not all(key in data for key in required_keys):
        print(f"Unexpected Finnhub response format for {symbol}. Keys received: {data.keys()}")
        return
    
    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    stock_id = cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,)).fetchone()[0]
    
    count = 0
    for i in range(len(data["t"])):
        if count >= 25:
            break
        try:
            date = datetime.fromtimestamp(data["t"][i]).strftime("%Y-%m-%d")
            cur.execute('''
            INSERT OR IGNORE INTO weekly_data 
            (stock_id, date, open, close, high, low, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_id, date,
                data["o"][i],
                data["c"][i],
                data["h"][i],
                data["l"][i],
                int(data["v"][i])
            ))
            if cur.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"Error inserting Finnhub data for {symbol}: {e}")
    
    cur.execute('''
    INSERT OR REPLACE INTO api_metadata 
    (stock_id, api_name, last_updated)
    VALUES (?, ?, ?)
    ''', (stock_id, "Finnhub", datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"Inserted {count} new rows for {symbol} (Finnhub).")

def insert_financialdatasets_data(symbol):
    data = fetch_financialdatasets_data(symbol)
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    
    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    stock_id = cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,)).fetchone()[0]
    
    count = 0
    for entry in data["results"]:
        if count >= 25:
            break
        try:
            cur.execute('''
            INSERT OR IGNORE INTO weekly_data 
            (stock_id, date, open, close, high, low, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stock_id, entry["date"],
                entry["open"],
                entry["close"],
                entry["high"],
                entry["low"],
                entry["volume"]
            ))
            if cur.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"Error inserting {entry['date']}: {e}")
    
    cur.execute('''
    INSERT OR REPLACE INTO api_metadata 
    (stock_id, api_name, last_updated)
    VALUES (?, ?, ?)
    ''', (stock_id, "FinancialDatasets.ai", datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"Inserted {count} new rows for {symbol} (FinancialDatasets.ai).")

if __name__ == "__main__":
    setup_database()  # Ensure the database is set up
    symbols = ["AAPL", "MSFT", "TSLA"]
    for symbol in symbols:
        insert_alpha_vantage_data(symbol)
        insert_yahoo_data(symbol)
        insert_finnhub_data(symbol)
        insert_financialdatasets_data(symbol)