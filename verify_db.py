import sqlite3

try:
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    conn.close()
except sqlite3.Error as e:
    print(f"Database error: {e}")
