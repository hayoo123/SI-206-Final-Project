import sqlite3

def setup_database():
    conn = sqlite3.connect('stocks.db')
    cur = conn.cursor()

    # Create stocks table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS weekly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            date TEXT,
            open REAL,
            close REAL,
            high REAL,
            low REAL,
            volume INTEGER,
            UNIQUE(stock_id, date),
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()

