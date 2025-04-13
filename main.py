from db_insert import insert_alpha_weekly_data
from visualize import plot_price

if __name__ == "__main__":
    symbol = "AAPL"
    insert_alpha_weekly_data(symbol)

    # Visualizations
    plot_price(symbol, "close", "Closing", "blue")
    plot_price(symbol, "open", "Opening", "green")
    plot_price(symbol, "high_low_avg", "High-Low Average", "purple")
