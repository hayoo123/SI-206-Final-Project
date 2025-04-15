import matplotlib.pyplot as plt
import pandas as pd
from data import fetch_alpha_vantage_data, fetch_yahoo_data, fetch_financialdatasets_data

def plot_high_low_avg_comparison(symbol):
    # Fetch data from APIs
    alpha_data = fetch_alpha_vantage_data(symbol)
    yahoo_data = fetch_yahoo_data(symbol)
    financialdatasets_data = fetch_financialdatasets_data(symbol)
    
    # Process Alpha Vantage data
    alpha_series = alpha_data.get("Time Series (Daily)", {})
    alpha_dates = []
    alpha_avg = []
    for date, metrics in sorted(alpha_series.items()):
        high = float(metrics["2. high"])
        low = float(metrics["3. low"])
        avg = (high + low) / 2
        alpha_dates.append(date)
        alpha_avg.append(avg)
    
    # Process Yahoo Finance data
    yahoo_avg = []
    yahoo_dates = [d.strftime('%Y-%m-%d') for d in yahoo_data.index]
    for high, low in zip(yahoo_data['High'], yahoo_data['Low']):
        avg = (high + low) / 2
        yahoo_avg.append(avg)
    
    # Process FinancialDatasets.ai data
    financialdatasets_avg = []
    financialdatasets_dates = [entry['time'].split('T')[0] for entry in financialdatasets_data['prices']]
    for entry in financialdatasets_data['prices']:
        avg = (entry['high'] + entry['low']) / 2
        financialdatasets_avg.append(avg)
    
    # Print data for debugging
    print(f"Alpha Vantage Dates: {alpha_dates}")
    print(f"Alpha Vantage Avg: {alpha_avg}")
    print(f"Yahoo Finance Dates: {yahoo_dates}")
    print(f"Yahoo Finance Avg: {yahoo_avg}")
    print(f"FinancialDatasets Dates: {financialdatasets_dates}")
    print(f"FinancialDatasets Avg: {financialdatasets_avg}")
    
    # Plot data
    plt.figure(figsize=(14, 8))
    plt.plot(alpha_dates, alpha_avg, marker='o', linestyle='-', color='blue', label='Alpha Vantage')
    plt.plot(yahoo_dates, yahoo_avg, marker='x', linestyle='-', color='orange', label='Yahoo Finance')
    plt.plot(financialdatasets_dates, financialdatasets_avg, marker='d', linestyle='-', color='green', label='FinancialDatasets.ai')
    plt.title(f"{symbol} Weekly Average High-Low Comparison", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Avg High-Low Price ($)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    for symbol in symbols:
        plot_high_low_avg_comparison(symbol)
