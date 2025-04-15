import matplotlib.pyplot as plt
import seaborn as sns
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

if __name__ == "__main__":
    plot_price_comparison()
    plot_volatility_comparison()
    plot_success_count()
