import sqlite3
import os

def scan_backups():
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        print("No backups folder found.")
        return

    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    print(f"Scanning {len(backups)} backups...\n")

    results = []
    for f in backups:
        path = os.path.join(backup_dir, f)
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            
            # Check for core tables
            tables = ['customers', 'invoices', 'payments', 'financial_records', 'inventory', 'quotations']
            counts = {}
            for t in tables:
                try:
                    cursor.execute(f"SELECT count(*) FROM {t}")
                    counts[t] = cursor.fetchone()[0]
                except Exception:
                    counts[t] = '?'
            
            results.append((f, counts))
            conn.close()
        except Exception as e:
            print(f"Error reading {f}: {e}")

    # Sort by number of invoices + payments as a proxy for "most data"
    def score(row):
        counts = row[1]
        s = 0
        for k in ['invoices', 'payments', 'customers', 'inventory']:
            val = counts.get(k, 0)
            if isinstance(val, int):
                s += val
        return s

    results.sort(key=score, reverse=True)

    print(f"{'Backup File':<40} | {'Cust':<4} | {'Inv':<4} | {'Pay':<4} | {'Fin':<4} | {'Stocks':<4} | {'Quot':<4}")
    print("-" * 100)
    for f, c in results:
        print(f"{f:<40} | {c.get('customers','0'):<4} | {c.get('invoices','0'):<4} | {c.get('payments','0'):<4} | {c.get('financial_records','0'):<4} | {c.get('inventory','0'):<4} | {c.get('quotations','0'):<4}")

if __name__ == "__main__":
    scan_backups()
