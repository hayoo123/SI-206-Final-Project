import sqlite3
import matplotlib.pyplot as plt
from data import fetch_alpha_vantage_data, fetch_yahoo_data

def plot_price(symbol, column, title, color):
    """Plot specified column (open, close, high-low avg) for a stock."""
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()

    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol,))
    stock_id = cur.fetchone()[0]

    if column == "high_low_avg":
        cur.execute("""
            SELECT date, high, low FROM weekly_data 
            WHERE stock_id = ? 
            ORDER BY date ASC 
            LIMIT 25
        """, (stock_id,))
        rows = cur.fetchall()
        dates = [row[0] for row in rows]
        values = [(row[1] + row[2]) / 2 for row in rows]
    else:
        cur.execute(f"""
            SELECT date, {column} FROM weekly_data 
            WHERE stock_id = ? 
            ORDER BY date ASC 
            LIMIT 25
        """, (stock_id,))
        rows = cur.fetchall()
        dates = [row[0] for row in rows]
        values = [row[1] for row in rows]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o', linestyle='-', color=color)
    plt.title(f"{symbol} Weekly {title} Prices")
    plt.xlabel("Date")
    plt.ylabel(f"{title} Price ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    conn.close()

# Line chart
def plot_high_low_avg_comparison(symbol):
    alpha_data = fetch_alpha_vantage_data(symbol)
    alpha_series = alpha_data.get("Weekly Time Series", {})
    alpha_dates = []
    alpha_avg = []

    for date, metrics in sorted(alpha_series.items())[:6]:
        high = float(metrics["2. high"])
        low = float(metrics["3. low"])
        avg = (high + low) / 2
        alpha_dates.append(date)
        alpha_avg.append(avg)

    yahoo_data = fetch_yahoo_data(symbol)
    yahoo_avg = []
    yahoo_dates = [d.strftime('%Y-%m-%d') for d in yahoo_data.index]

    for high, low in zip(yahoo_data['High'], yahoo_data['Low']):
        avg = (high + low) / 2
        yahoo_avg.append(avg)

    plt.figure(figsize=(12, 6))
    plt.plot(alpha_dates, alpha_avg, marker='o', label='Alpha Vantage')
    plt.plot(yahoo_dates, yahoo_avg, marker='x', label='Yahoo Finance')
    plt.title(f"{symbol} Weekly Average High-Low Comparison")
    plt.xlabel("Date")
    plt.ylabel("Avg High-Low Price ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()
