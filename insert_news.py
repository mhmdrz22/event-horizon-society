import sqlite3
import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Check if the user with id=1 exists, otherwise the foreign key constraint will fail
cursor.execute("SELECT id FROM users WHERE id = 1")
user = cursor.fetchone()

if user:
    cursor.execute("""
    INSERT INTO news (title, content, status, author_id, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ('Test News', 'This is a test news item', 'published', 1, datetime.datetime.now(), datetime.datetime.now()))

    conn.commit()
    print("Test news item inserted successfully.")
else:
    print("User with id=1 not found. Cannot insert news item.")

conn.close()
