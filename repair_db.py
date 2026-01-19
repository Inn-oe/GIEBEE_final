import pandas as pd
import sqlite3
import os

def repair_database():
    db_path = 'instance/database.db'
    excel_path = 'data/inventory.xlsx'
    
    if not os.path.exists(db_path) or not os.path.exists(excel_path):
        print("Required files for repair not found.")
        return

    print("Repairing local database using Excel backups...")
    
    # Load inventory from Excel
    df = pd.read_excel(excel_path)
    if df.empty:
        print("Inventory Excel is empty.")
        return
        
    conn = sqlite3.connect(db_path)
    
    # Insert missing inventory items
    try:
        # We use 'to_sql' with 'append' but we need to match columns
        # Alternatively, individual inserts for safety
        cursor = conn.cursor()
        for _, row in df.iterrows():
            try:
                # Check if exists
                cursor.execute("SELECT id FROM inventory WHERE id = ?", (int(row['id']),))
                if not cursor.fetchone():
                    print(f"Restoring Inventory Item: {row['name']} (ID: {row['id']})")
                    # Dynamically build insert
                    cols = df.columns.tolist()
                    placeholders = ", ".join(["?"] * len(cols))
                    col_str = ", ".join(cols)
                    cursor.execute(f"INSERT INTO inventory ({col_str}) VALUES ({placeholders})", tuple(row))
            except Exception as e:
                print(f"Error restoring row: {e}")
        
        conn.commit()
    except Exception as e:
        print(f"Repair failed: {e}")
    finally:
        conn.close()
    
    print("Local database repair complete.")

if __name__ == "__main__":
    repair_database()
