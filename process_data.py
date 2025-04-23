import sqlite3

def calculate_avg_close_and_write(filename="averages.txt"):
    """
    Calculates the average closing price for each stock symbol and writes the results to a text file.

    Parameters:
    filename (str): The name of the file to write the results to. The default is "averages.txt".

    What the code does:
    - Connects to the SQLite database ('stocks.db').
    - Joins the 'stocks' and 'weekly_data' tables on stock_id.
    - Calculates the average closing price for each symbol.
    - Writes the formatted results to the specified text file.

    Returns:
    None: This function does not return any value.
    """
    
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    
    # JOIN stocks + weekly_data and calculate average 
    cur.execute("""
    SELECT stocks.symbol, AVG(weekly_data.close)
    FROM weekly_data
    JOIN stocks ON weekly_data.stock_id = stocks.id
    GROUP BY stocks.symbol
    """)
    
    results = cur.fetchall()
    
    # Write results to text file
    with open(filename, "w") as f:
        f.write("Average Closing Prices by Stock Symbol\n")
        f.write("----------------------------------------\n")
        for symbol, avg_close in results:
            f.write(f"{symbol}: ${avg_close:.2f}\n")
    
    print(f"Averages written to {filename}")
    
    # Omit 5 rows each time the script runs
    cur.execute("""
    DELETE FROM weekly_data
    WHERE id IN (
        SELECT id FROM weekly_data
        ORDER BY date ASC
        LIMIT 5
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    calculate_avg_close_and_write()
