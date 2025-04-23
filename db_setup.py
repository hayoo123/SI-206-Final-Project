import sqlite3

def setup_database():
     """
    Initializes the SQLite database by creating necessary tables if they do not exist.

    Parameters: None

    What the code does:
    - Connects to a database named 'stocks.db'.
    - Creates the 'stocks' table with 'id' and 'symbol'.
    - Creates the 'weekly_data' table with stock metrics and a foreign key reference to 'stocks'.

    Returns:
    None: This function does not return any value. 
    """
    
    conn = sqlite3.connect("stocks.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weekly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            UNIQUE(stock_id, date),
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
