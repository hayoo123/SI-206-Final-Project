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

### NEW GRAPHS###
# Graph 1: Line chart of last week high and low average prices per API
def plot_high_low_avg_comparison(symbol, start_date, end_date):
    # Fetch data
    alpha_data = fetch_alpha_vantage_data(symbol)
    yahoo_data = fetch_yahoo_data(symbol)
    financialdatasets_data = fetch_financialdatasets_data(symbol, start_date, end_date)
    polygon_data = fetch_polygon_daily_data(symbol, start_date, end_date)
    
    # Process Alpha data
    alpha_series = alpha_data.get("Time Series (Daily)", {})
    alpha_dates = []
    alpha_avg = []
    for date, metrics in sorted(alpha_series.items()):
        high = float(metrics["2. high"])
        low = float(metrics["3. low"])
        avg = (high + low) / 2
        alpha_dates.append(date)
        alpha_avg.append(avg)

    # Process Yahoo data
    yahoo_avg = []
    yahoo_dates = [d.strftime('%Y-%m-%d') for d in yahoo_data.index]
    for high, low in zip(yahoo_data['High'], yahoo_data['Low']):
        avg = (high + low) / 2
        yahoo_avg.append(avg)
    
    # Process FinancialDatasets data
    financialdatasets_avg = []
    financialdatasets_dates = [entry['time'].split('T')[0] for entry in financialdatasets_data['prices']]
    for entry in financialdatasets_data['prices']:
        avg = (entry['high'] + entry['low']) / 2
        financialdatasets_avg.append(avg)
    
    # Process Polygon data
    polygon_avg = []
    polygon_dates = [pd.to_datetime(entry["t"], unit="ms").strftime('%Y-%m-%d') for entry in polygon_data['results']]
    for entry in polygon_data['results']:
        avg = (entry['h'] + entry['l']) / 2
        polygon_avg.append(avg)
    
    # Combine data into DataFrame
    plot_df = pd.DataFrame({
        'Alpha Vantage': pd.Series(alpha_avg, index=alpha_dates),
        'Yahoo Finance': pd.Series(yahoo_avg, index=yahoo_dates),
        'FinancialDatasets.ai': pd.Series(financialdatasets_avg, index=financialdatasets_dates),
        'Polygon.io': pd.Series(polygon_avg, index=polygon_dates)
    }).sort_index()
    
    # Plot data
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=plot_df, markers=True, dashes=False, palette='tab10')
    plt.title(f"{symbol} High-Low Average Comparison (Past Week)", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Avg High-Low Price ($)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Data Source', fontsize=12)
    plt.tight_layout()
    plt.grid(True)
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
    # Plot
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

    # Plot
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
            if api_name == "Alpha Vantage" or api_name == "Yahoo Finance":
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

# Graph 5: Timestamps returned per API
def plot_timestamp_coverage(symbol="AAPL"):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')

    alpha_data = fetch_alpha_vantage_data(symbol).get("Weekly Time Series", {})
    alpha_dates = list(alpha_data.keys())
    
    yahoo_df = fetch_yahoo_data(symbol, period="30d")
    yahoo_dates = yahoo_df.index.strftime('%Y-%m-%d').tolist()
    
    polygon_data = fetch_polygon_daily_data(symbol, start, end).get("results", [])
    polygon_dates = [pd.to_datetime(entry["t"], unit="ms").strftime('%Y-%m-%d') for entry in polygon_data]
    
    fd_data = fetch_financialdatasets_data(symbol, start, end).get("prices", [])
    fd_dates = [entry["time"] for entry in fd_data if "time" in entry]

    # Count unique dates
    timestamp_counts = {
        "Alpha Vantage": len(set(alpha_dates)),
        "Yahoo Finance": len(set(yahoo_dates)),
        "Polygon.io": len(set(polygon_dates)),
        "FinancialDatasets": len(set(fd_dates))
    }

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(timestamp_counts.keys(), timestamp_counts.values(), color='skyblue')
    plt.title(f"Number of Unique Timestamps Returned (Last 30 Days) - {symbol}")
    plt.ylabel("Unique Dates")
    plt.xlabel("API")
    plt.ylim(0, 35)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    symbol = "AAPL"
    plot_high_low_avg_comparison("AAPL", start_date, end_date)
    plot_volatility_comparison()
    plot_success_count()
    plot_api_latency(symbol)
    plot_timestamp_coverage()
