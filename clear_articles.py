import sqlite3

try:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    conn.commit()
    print("Successfully cleared articles table.")
    cursor.execute("SELECT COUNT(*) FROM articles")
    print(f"Row count now: {cursor.fetchone()[0]}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
