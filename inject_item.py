import sqlite3
import os

db_path = 'instance/database.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("INSERT OR REPLACE INTO inventory (id, name, quantity, unit_price) VALUES (1, 'lithium battery', 10, 350.0)")
        conn.commit()
        print("Successfully injected missing inventory ID: 1")
    except Exception as e:
        print(f"Injection failed: {e}")
    finally:
        conn.close()
