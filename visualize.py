import sqlite3
import matplotlib.pyplot as plt

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
