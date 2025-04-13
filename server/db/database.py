# server/db/database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("sales.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            stock INTEGER,
            discount TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            text TEXT,
            sender TEXT,
            sentiment TEXT,
            timestamp DATETIME
        )
    """)
    # Insert sample products
    conn.execute("""
        INSERT OR IGNORE INTO products (id, name, price, stock, discount) VALUES
        ('1', 'Laptop', 999.0, 30, '0%'),
        ('2', 'Phone', 599.0, 50, '0%'),
        ('3', 'Tablet', 399.0, 20, '0%'),
        ('4', 'Headphones', 199.0, 100, '5%'),
        ('5', 'Camera', 799.0, 10, '0%')
    """)
    conn.commit()
    conn.close()
