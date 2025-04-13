# Run in a Python shell or save as a script (e.g., check_db.py) and run with `python check_db.py`
import sqlite3

conn = sqlite3.connect("D:/Angular/ai-sales-bot/server/sales.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()
print("Products in database:")
for row in rows:
    print(row)
conn.close()
