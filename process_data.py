import sqlite3

def calculate_avg_close_and_write(filename="averages.txt"):
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
