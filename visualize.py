import matplotlib.pyplot as plt
import pandas as pd
from data import (
    fetch_alpha_vantage_data,
    fetch_yahoo_data,
    fetch_financialdatasets_data,
    fetch_polygon_daily_data
)

def plot_alpha_vantage(symbol):
    data = fetch_alpha_vantage_data(symbol)
    series = data.get("Weekly Time Series", {})
    
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
    df.index = pd.to_datetime(df.index)
    weekly_df = df['Close'].resample('W').last()  # Weekly closing prices
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
    data = fetch_polygon_daily_data(symbol)
    results = data.get("results", [])

    if not results:
        print("No data returned from Polygon.io.")
        return

    # Grab the last 6 entries (in ascending date order)
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
    data = fetch_financialdatasets_data(symbol)
    prices = data.get('prices', [])
    if not prices:
        print("No data returned from FinancialDatasets.ai.")
        return

    print("First price entry keys:", prices[0].keys())  # optional: can remove this now

    last_entries = prices[-6:]
    dates = []
    closes = []

    for entry in last_entries:
        # Grab the 'time' field
        date = entry.get('time')
        close = entry.get('close')
        if date and close:
            dates.append(date)
            closes.append(close)

    if not dates:
        print("No valid date/close pairs found in FinancialDatasets.ai data.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, marker='o', color='purple', label='FinancialDatasets.ai')
    plt.title(f"{symbol} - FinancialDatasets.ai Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()



# Run all graphs for a given stock
if __name__ == "__main__":
    symbol = "AAPL"
    plot_alpha_vantage(symbol)
    plot_yahoo_finance(symbol)
    plot_polygon_data(symbol)
    plot_financialdatasets(symbol)



############ addition ########
import matplotlib.pyplot as plt

# Replace these with your actual fetch functions
api_names = ['Alpha Vantage', 'Yahoo Finance', 'Polygon.io', 'FinancialDatasets']
timeframes = {'7d': 7, '30d': 30, '90d': 90, '180d': 180, '365d': 365}
data_counts = {api: [] for api in api_names}

# Simulated data counts (replace with real API responses)
data_counts['Alpha Vantage'] = [7, 7, 7, 7, 7]  # Weekly only
data_counts['Yahoo Finance'] = [7, 30, 90, 180, 365]
data_counts['Polygon.io'] = [7, 30, 90, 180, 365]
data_counts['FinancialDatasets'] = [7, 30, 90, 180, 250]  # Maybe limited

# Plotting
plt.figure(figsize=(12, 6))
for api in api_names:
    plt.plot(list(timeframes.keys()), data_counts[api], label=api, marker='o')

plt.title("Number of Data Points Returned by Each API Across Timeframes")
plt.xlabel("Timeframe")
plt.ylabel("Data Points Returned")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

############

import matplotlib.pyplot as plt
import pandas as pd

# Simulated success/failure data (1 = success, 0 = fail)
stocks = ["AAPL", "TSLA", "MSFT", "NVDA", "GOOGL"]
success_data = {
    "Alpha Vantage": [1, 1, 1, 1, 1],
    "Yahoo Finance": [1, 1, 1, 1, 1],
    "FinancialDatasets": [1, 0, 1, 0, 1],
    "Polygon.io": [1, 1, 1, 1, 1]
}

success_df = pd.DataFrame(success_data, index=stocks)
success_counts = success_df.sum().sort_values(ascending=False)

# Plotting
plt.figure(figsize=(8, 5))
success_counts.plot(kind='bar', color='mediumseagreen')
plt.title("Successful API Fetches per Platform")
plt.ylabel("Number of Successful Calls (out of 5 stocks)")
plt.xlabel("API Platform")
plt.ylim(0, 5.5)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#######
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import random

# Simulated standard deviation (volatility) for each stock per API
stocks = ["AAPL", "TSLA", "MSFT", "NVDA", "GOOGL"]
volatility_data = {
    "Alpha Vantage": [random.uniform(2, 5) for _ in stocks],
    "Yahoo Finance": [random.uniform(1.5, 4) for _ in stocks],
    "FinancialDatasets": [random.uniform(1.8, 4.5) for _ in stocks],
    "Polygon.io": [random.uniform(2, 4.2) for _ in stocks]
}
vol_df = pd.DataFrame(volatility_data, index=stocks)

# Prepare data for Seaborn
melted_vol = vol_df.reset_index().melt(id_vars="index", var_name="API", value_name="Volatility")
melted_vol.rename(columns={"index": "Stock"}, inplace=True)

# Plotting
plt.figure(figsize=(10, 6))
sns.boxplot(data=melted_vol, x="API", y="Volatility", palette="pastel")
plt.title("Volatility (Price Std Dev) by API")
plt.xlabel("API Platform")
plt.ylabel("Volatility ($)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
