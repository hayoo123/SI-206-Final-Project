import sqlite3
from data import fetch_alpha_vantage_data

def insert_alpha_weekly_data(symbol):
    """Insert Alpha Vantage weekly stock data into the database."""
    data = fetch_alpha_vantage_data(symbol)
    time_series = data.get("Weekly Time Series", {})

    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY, symbol TEXT UNIQUE)")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS weekly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            date TEXT,
            open REAL,
            close REAL,
            high REAL,
            low REAL,
            volume INTEGER,
            UNIQUE(stock_id, date),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
        )
    ''')

    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

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
            count += 1
        except Exception as e:
            print(f"Error inserting {date}: {e}")
    conn.commit()
    conn.close()
    print(f"Inserted {count} new rows for {symbol}.")
