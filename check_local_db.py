import sqlite3
import os

db_path = 'instance/database.db'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
    
    print(f"Checking database: {db_path}")
    print("-" * 30)
    for table in tables:
        try:
            cursor.execute(f"SELECT count(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:<20} | {count}")
        except Exception as e:
            print(f"{table:<20} | Error: {e}")
    conn.close()
