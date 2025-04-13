# fix_product_id.py
import sqlite3

conn = sqlite3.connect("D:/Angular/ai-sales-bot/server/sales.db")
cursor = conn.cursor()

# Delete the incorrect product
cursor.execute("DELETE FROM products WHERE id = ?", ('1744506217443',))

# Get the highest ID and add the product with the next ID
cursor.execute("SELECT MAX(CAST(id AS INTEGER)) FROM products")
max_id = cursor.fetchone()[0]  # Should be 5
new_id = str(max_id + 1)  # Should be 6
cursor.execute(
    "INSERT INTO products (id, name, price, stock, discount) VALUES (?, ?, ?, ?, ?)",
    (new_id, "nano super", 250.0, 0, "0")
)

conn.commit()
conn.close()
print("Product ID fixed.")