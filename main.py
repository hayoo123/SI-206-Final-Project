from db_insert import insert_alpha_weekly_data
from visualize import (
    plot_price,
    plot_high_low_avg_comparison,
    plot_avg_close_bar,
    plot_volume_pie,
    plot_multi_symbol_trend,
    save_to_csv
)

if __name__ == "__main__":
    # Step 1: Insert data for multiple symbols
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]  # Add more as needed
    for symbol in symbols:
        insert_alpha_weekly_data(symbol)
    
    # Step 2: Generate CSV and plots for one symbol (avoid redundancy)
    symbol = "AAPL"
    save_to_csv(symbol)  # New CSV export
    
    # Existing visualizations (now using JOIN queries)
    plot_price(symbol, "close", "Closing", "blue")
    plot_high_low_avg_comparison(symbol)
    plot_avg_close_bar(symbol)
    plot_volume_pie(symbol)
    plot_multi_symbol_trend(["AAPL", "MSFT"])