import sqlite3
from data import fetch_alpha_vantage_data

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

        # Extract and convert values
        try:
            open_price = float(metrics["1. open"])
            high = float(metrics["2. high"])
            low = float(metrics["3. low"])
            close = float(metrics["4. close"])
            volume = int(metrics["5. volume"])
        except Exception as e:
            print(f"Skipping {date} due to error: {e}")
            continue

        # Insert row if not a duplicate
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
    conn.close()
    print(f"Inserted {count} new rows for {symbol}")

if __name__ == "__main__":
    insert_alpha_data("AAPL")  # Replace with any other stock symbol if needed
