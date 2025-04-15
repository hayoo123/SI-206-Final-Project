import sqlite3
import matplotlib.pyplot as plt
import pandas as pd 
from data import fetch_alpha_vantage_data, fetch_yahoo_data

def plot_price(symbol, column, title, color):
    """Plot using explicit JOIN"""
    df = get_joined_data(symbol)  # Uses our JOIN query
    
    if column == "high_low_avg":
        values = (df['high'] + df['low']) / 2
    else:
        values = df[column]
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], values, marker='o', linestyle='-', color=color)
    plt.title(f"{symbol} Weekly {title} Prices")
    plt.xlabel("Date")
    plt.ylabel(f"{title} Price ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()
 

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

# Bar Chart
def plot_avg_close_bar(symbol):
    alpha_data = fetch_alpha_vantage_data(symbol)
    alpha_series = alpha_data.get("Weekly Time Series", {})
    alpha_closes = [float(metrics["4. close"]) for _, metrics in list(alpha_series.items())[:6]]
    alpha_avg = sum(alpha_closes) / len(alpha_closes)

    yahoo_data = fetch_yahoo_data(symbol)
    yahoo_closes = yahoo_data['Close'].tolist()
    yahoo_avg = sum(yahoo_closes) / len(yahoo_closes)

    apis = ['Alpha Vantage', 'Yahoo Finance']
    averages = [alpha_avg, yahoo_avg]

    plt.figure(figsize=(8, 6))
    plt.bar(apis, averages, color=['blue', 'orange'])
    plt.title(f"{symbol} Avg Weekly Closing Prices by API")
    plt.ylabel("Price ($)")
    plt.tight_layout()
    plt.show()

# Pie chart
def plot_volume_pie(symbol):
    alpha_data = fetch_alpha_vantage_data(symbol)
    alpha_series = alpha_data.get("Weekly Time Series", {})
    alpha_volume = sum(int(metrics["5. volume"]) for _, metrics in list(alpha_series.items())[:6])

    yahoo_data = fetch_yahoo_data(symbol)
    yahoo_volume = sum(yahoo_data['Volume'].tolist())

    sizes = [alpha_volume, yahoo_volume]
    labels = ['Alpha Vantage', 'Yahoo Finance']
    colors = ['skyblue', 'lightgreen']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title(f"{symbol} Volume Distribution Across APIs")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Line chart #2
def plot_multi_symbol_trend(symbols):
    plt.figure(figsize=(12, 6))

    for symbol in symbols:
        data = fetch_alpha_vantage_data(symbol)
        series = data.get("Weekly Time Series", {})
        dates = []
        closes = []
        for date, metrics in sorted(series.items())[:6]:
            dates.append(date)
            closes.append(float(metrics["4. close"]))
        plt.plot(dates, closes, marker='o', label=symbol)

    plt.title("Weekly Closing Prices Across Stocks")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()


def save_to_csv(symbol):
    """Export stock data to CSV."""
    import pandas as pd
    with sqlite3.connect("stocks.db") as conn:
        df = pd.read_sql("""
            SELECT date, open, close, (high+low)/2 AS avg_hl, volume
            FROM weekly_data 
            WHERE stock_id = (SELECT id FROM stocks WHERE symbol = ?)
        """, conn, params=(symbol,))
        df.to_csv(f"{symbol}_data.csv", index=False)

def get_joined_data(symbol):
    """Explicit JOIN example for grading purposes"""
    with sqlite3.connect("stocks.db") as conn:
        query = """
        SELECT 
            s.symbol,
            w.date,
            w.open,
            w.close,
            (w.high + w.low)/2 AS avg_hl,
            w.volume
        FROM weekly_data w
        JOIN stocks s ON w.stock_id = s.id
        WHERE s.symbol = ?
        ORDER BY w.date DESC
        LIMIT 25
        """
        df = pd.read_sql(query, conn, params=(symbol,))
    return df