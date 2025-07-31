import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute("UPDATE news SET status = 'PUBLISHED' WHERE status = 'published'")

conn.commit()
print(f"{cursor.rowcount} news item(s) updated.")
conn.close()
