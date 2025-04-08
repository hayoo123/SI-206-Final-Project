# Names: Hannah Yoo, Hannah Cooper, Valentina Rivano 
from data import fetch_alpha_vantage_data, fetch_yahoo_data

symbol = "AAPL"  # or any stock symbol

# Alpha Vantage
alpha_data = fetch_alpha_vantage_data(symbol)
print("Alpha Vantage Weekly Data:")
print(alpha_data)

# Yahoo Finance
yahoo_data = fetch_yahoo_data(symbol)
print("\nYahoo Finance 7-Day Data:")
print(yahoo_data)



from data import fetch_alpha_vantage_data

symbol = "AAPL"
data = fetch_alpha_vantage_data(symbol)
print(data)

