import sqlite3

def verify_join():
    with sqlite3.connect("stocks.db") as conn:
        cur = conn.cursor()
        
        # Explicit JOIN query
        cur.execute("""
        SELECT s.symbol, COUNT(*) as record_count
        FROM weekly_data w
        JOIN stocks s ON w.stock_id = s.id
        GROUP BY s.symbol
        """)
        
        print("JOIN Verification Results:")
        print("{:<6} {:<12}".format("Symbol", "Records"))
        print("-"*18)
        for row in cur.fetchall():
            print("{:<6} {:<12}".format(row[0], row[1]))

if __name__ == "__main__":
    verify_join()