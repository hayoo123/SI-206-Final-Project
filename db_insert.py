import sqlite3
from data import fetch_alpha_vantage_data
from contextlib import closing

def insert_alpha_weekly_data(symbol, weeks_limit=25):
    """Insert Alpha Vantage weekly stock data into the database."""
    data = fetch_alpha_vantage_data(symbol)
    time_series = data.get("Weekly Time Series", {})

    with closing(sqlite3.connect("stocks.db")) as conn:
        cur = conn.cursor()
        
        # Ensure stock exists
        cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
        stock_id = cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,)).fetchone()[0]

        # Insert weekly data
        count = 0
        for date, metrics in sorted(time_series.items(), reverse=True):
            if count >= weeks_limit:
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
            except (ValueError, KeyError) as e:
                print(f"Skipping {date}: Invalid data format - {e}")
            except sqlite3.Error as e:
                print(f"Database error on {date}: {e}")

        conn.commit()
        print(f"Inserted {count} new weekly records for {symbol}")