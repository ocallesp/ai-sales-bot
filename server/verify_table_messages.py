import sqlite3
conn = sqlite3.connect("D:/Angular/ai-sales-bot/server/sales.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()
print("Messages in database:")
for row in rows:
    print(row)
conn.close()
