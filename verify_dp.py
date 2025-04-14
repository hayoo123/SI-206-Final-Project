import sqlite3

with sqlite3.connect("stocks.db") as conn:
    # Check total rows
    total_rows = conn.execute("SELECT COUNT(*) FROM weekly_data").fetchone()[0]
    print(f"Total weekly_data rows: {total_rows} (should be >=100)")
    
    # Check rows per symbol
    for symbol in ["AAPL", "MSFT", "GOOGL", "TSLA"]:
        count = conn.execute("""
            SELECT COUNT(*) 
            FROM weekly_data w
            JOIN stocks s ON w.stock_id = s.id
            WHERE s.symbol = ?
        """, (symbol,)).fetchone()[0]
        print(f"{symbol}: {count} rows")


with sqlite3.connect("stocks.db") as conn:
    # Count total records
    total = conn.execute("SELECT COUNT(*) FROM weekly_data").fetchone()[0]
    print(f"Total weekly records: {total} (should be 100)")
    
    # Count per symbol
    for symbol in ["AAPL", "MSFT", "GOOGL", "TSLA"]:
        count = conn.execute("""
            SELECT COUNT(*) 
            FROM weekly_data w
            JOIN stocks s ON w.stock_id = s.id
            WHERE s.symbol = ?
        """, (symbol,)).fetchone()[0]
        print(f"{symbol}: {count} records")