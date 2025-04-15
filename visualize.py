import matplotlib.pyplot as plt
import seaborn as sns
import time
import pandas as pd
from datetime import datetime, timedelta
from data import (
    fetch_alpha_vantage_data,
    fetch_yahoo_data,
    fetch_financialdatasets_data,
    fetch_polygon_daily_data
)

symbol = "AAPL"
end_date = datetime.now()
start_date = end_date - timedelta(days=90)
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

#### PLOTTING ALL LINE GRAPHS ####
def plot_alpha_vantage(symbol):
    data = fetch_alpha_vantage_data(symbol)
    series = data.get("Weekly Time Series", {})
    
    if not series:
        print("No data returned from Alpha Vantage.")
        return

    dates = []
    closes = []

    for date, metrics in sorted(series.items(), reverse=True)[:6]:
        dates.append(date)
        closes.append(float(metrics["4. close"]))

    dates.reverse()
    closes.reverse()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, marker='o', label='Alpha Vantage', color='blue')
    plt.title(f"{symbol} - Alpha Vantage Weekly Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_yahoo_finance(symbol):
    df = fetch_yahoo_data(symbol)
    if df.empty:
        print("No data returned from Yahoo Finance.")
        return

    df.index = pd.to_datetime(df.index)
    weekly_df = df['Close'].resample('W').last()
    dates = weekly_df.index.strftime('%Y-%m-%d').tolist()[-6:]
    closes = weekly_df.tolist()[-6:]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, marker='o', color='orange', label='Yahoo Finance')
    plt.title(f"{symbol} - Yahoo Finance Weekly Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_polygon_data(symbol):
    end = datetime.now()
    start = end - timedelta(days=10)
    data = fetch_polygon_daily_data(symbol, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    results = data.get("results", [])

    if not results:
        print("No data returned from Polygon.io.")
        return

    last_entries = results[-6:]
    dates = [pd.to_datetime(entry["t"], unit="ms").strftime('%Y-%m-%d') for entry in last_entries]
    closes = [entry["c"] for entry in last_entries]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, marker='o', color='darkred', label='Polygon.io')
    plt.title(f"{symbol} - Polygon.io Daily Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_financialdatasets(symbol):
    end = datetime.now()
    start = end - timedelta(days=10)
    data = fetch_financialdatasets_data(symbol, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    prices = data.get('prices', [])

    if not prices:
        print("No data returned from FinancialDatasets.ai.")
        return

    last_entries = prices[-6:]
    dates = []
    closes = []

    for entry in last_entries:
        date = entry.get('time')
        close = entry.get('close')
        if date and close:
            dates.append(date)
            closes.append(close)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, marker='o', color='purple', label='FinancialDatasets.ai')
    plt.title(f"{symbol} - FinancialDatasets.ai Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

### NEW GRAPHS###

# Graph 1: Line chart of last 6 closing prices per API
def plot_price_comparison():
    av_data = fetch_alpha_vantage_data(symbol).get("Weekly Time Series", {})
    fd_data = fetch_financialdatasets_data(symbol, start_str, end_str).get("prices", [])
    poly_data = fetch_polygon_daily_data(symbol, start_str, end_str).get("results", [])
    yf_data = fetch_yahoo_data(symbol, period="90d")

    plot_df = pd.DataFrame()

    if av_data:
        av_closes = [(d, float(av_data[d]["4. close"])) for d in sorted(av_data.keys(), reverse=True)[:6]]
        plot_df['Alpha Vantage'] = pd.Series({d: c for d, c in av_closes})

    if fd_data:
        fd_closes = [(entry["time"], entry["close"]) for entry in fd_data][-6:]
        plot_df['FinancialDatasets'] = pd.Series({d: c for d, c in fd_closes})

    if poly_data:
        poly_closes = [(pd.to_datetime(entry["t"], unit="ms").strftime('%Y-%m-%d'), entry["c"]) for entry in poly_data][-6:]
        plot_df['Polygon.io'] = pd.Series({d: c for d, c in poly_closes})

    if not yf_data.empty:
        yf_week = yf_data['Close'].resample('W').last().dropna()
        yf_closes = yf_week[-6:]
        plot_df['Yahoo Finance'] = yf_closes

    plot_df = plot_df.sort_index()
    plot_df.plot(figsize=(12, 6), marker='o')
    plt.title("Weekly Closing Prices - API Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Graph 2: Boxplot of volatility comparison

def plot_volatility_comparison():
    stocks = ["AAPL", "TSLA", "MSFT", "GOOGL"]
    rows = []

    for s in stocks:
        row = {}
        try:
            av = fetch_alpha_vantage_data(s).get("Weekly Time Series", {})
            av_prices = [float(v["4. close"]) for k, v in sorted(av.items(), reverse=True)[:6]]
            row["Alpha Vantage"] = pd.Series(av_prices).std()
        except:
            row["Alpha Vantage"] = None

        try:
            yf = fetch_yahoo_data(s, "90d")['Close'].resample('W').last().dropna()
            row["Yahoo Finance"] = yf.std()
        except:
            row["Yahoo Finance"] = None

        try:
            fd = fetch_financialdatasets_data(s, start_str, end_str).get("prices", [])
            fd_prices = [entry["close"] for entry in fd][-6:]
            row["FinancialDatasets"] = pd.Series(fd_prices).std()
        except:
            row["FinancialDatasets"] = None

        try:
            poly = fetch_polygon_daily_data(s, start_str, end_str).get("results", [])
            poly_prices = [entry["c"] for entry in poly][-6:]
            row["Polygon.io"] = pd.Series(poly_prices).std()
        except:
            row["Polygon.io"] = None

        row["Stock"] = s
        rows.append(row)

    df = pd.DataFrame(rows).set_index("Stock").dropna()
    melted = df.reset_index().melt(id_vars="Stock", var_name="API", value_name="Volatility")

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=melted, x="API", y="Volatility", palette="pastel")
    plt.title("Volatility (Standard Deviation) by API")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Graph 3: Bar chart of successful fetch counts

def plot_success_count():
    apis = ["Alpha Vantage", "Yahoo Finance", "FinancialDatasets", "Polygon.io"]
    stocks = ["AAPL", "TSLA", "MSFT", "GOOGL"]
    success = {api: 0 for api in apis}

    for stock in stocks:
        if fetch_alpha_vantage_data(stock).get("Weekly Time Series"): success["Alpha Vantage"] += 1
        if not fetch_yahoo_data(stock, "7d").empty: success["Yahoo Finance"] += 1
        if fetch_financialdatasets_data(stock, start_str, end_str).get("prices", []): success["FinancialDatasets"] += 1
        if fetch_polygon_daily_data(stock, start_str, end_str).get("results", []): success["Polygon.io"] += 1

    plt.figure(figsize=(8, 5))
    pd.Series(success).plot(kind="bar", color="mediumseagreen")
    plt.title("Successful Fetch Count by API")
    plt.ylabel("Successful Fetches (out of 4)")
    plt.ylim(0, 5)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

# Graph 4: Time each API takes to respond
def plot_api_latency(symbol="AAPL"):
    """Compare response times (latency) for each API"""
    apis = {
        "Alpha Vantage": fetch_alpha_vantage_data,
        "Yahoo Finance": fetch_yahoo_data,
        "Polygon.io": fetch_polygon_daily_data,
        "FinancialDatasets": fetch_financialdatasets_data,
    }

    latencies = {}

    for api_name, fetch_func in apis.items():
        start = time.time()
        try:
            # Use dynamic arguments for different fetchers
            if api_name == "Yahoo Finance":
                fetch_func(symbol)
            else:
                fetch_func(symbol, "2024-01-01", "2024-01-07")
        except Exception as e:
            print(f"{api_name} error: {e}")
        end = time.time()
        latencies[api_name] = round(end - start, 3)

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.bar(latencies.keys(), latencies.values(), color='teal')
    plt.title("API Response Time Comparison")
    plt.ylabel("Time (seconds)")
    plt.xlabel("API")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    symbol = "AAPL"
    plot_alpha_vantage(symbol)
    plot_yahoo_finance(symbol)
    plot_polygon_data(symbol)
    plot_financialdatasets(symbol)
    plot_price_comparison()
    plot_volatility_comparison()
    plot_success_count()
    plot_api_latency(symbol)
