# db_insert.py
import sqlite3
from data import fetch_alpha_vantage_data

DB_NAME = "stocks.db"

def insert_alpha_weekly_data(symbol):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO stocks (symbol) VALUES (?)", (symbol,))
    conn.commit()

    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

    data = fetch_alpha_vantage_data(symbol)
    weekly_data = data.get("Weekly Time Series", {})

    count = 0
    for date, values in sorted(weekly_data.items(), reverse=True):
        if count >= 25:
            break
        try:
            cur.execute("""
                INSERT OR IGNORE INTO weekly_data
                (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                stock_id,
                date,
                float(values["1. open"]),
                float(values["2. high"]),
                float(values["3. low"]),
                float(values["4. close"]),
                int(values["5. volume"])
            ))
            count += 1
        except Exception as e:
            print(f"Error inserting data for {symbol} on {date}: {e}")

    conn.commit()
    conn.close()
    print(f"Inserted {count} records for {symbol}")

# Example 
if __name__ == "__main__":
    for symbol in ["AAPL", "MSFT", "GOOGL", "TSLA"]:
        insert_alpha_weekly_data(symbol)
