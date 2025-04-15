import sqlite3
import pandas as pd

def calculate_average_closing_price():
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    
    query = '''
    SELECT s.symbol, AVG(w.close) AS avg_close
    FROM weekly_data w
    JOIN stocks s ON w.stock_id = s.id
    GROUP BY s.symbol
    '''
    
    cur.execute(query)
    results = cur.fetchall()
    
    with open("average_closing_prices.txt", "w") as file:
        for symbol, avg_close in results:
            file.write(f"{symbol}: {avg_close}\n")
    
    conn.close()

if __name__ == "__main__":
    calculate_average_closing_price()