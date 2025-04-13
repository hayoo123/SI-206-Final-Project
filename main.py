from db_insert import insert_alpha_weekly_data
from visualize import (
    plot_price,
    plot_high_low_avg_comparison,
    plot_avg_close_bar,
    plot_volume_pie,
    plot_multi_symbol_trend
)

if __name__ == "__main__":
    symbol = "AAPL"

    insert_alpha_weekly_data(symbol)

    plot_price(symbol, "close", "Closing", "blue")
    plot_price(symbol, "open", "Opening", "green")
    plot_price(symbol, "high_low_avg", "High-Low Average", "purple")

    plot_high_low_avg_comparison(symbol)
    plot_avg_close_bar(symbol)
    plot_volume_pie(symbol)

    plot_multi_symbol_trend(["AAPL", "TSLA", "MSFT"])
