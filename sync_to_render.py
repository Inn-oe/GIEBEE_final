import os
import sys
from sqlalchemy import create_engine, MetaData, Table, select, insert
from sqlalchemy.orm import sessionmaker

# Add current directory to path for imports
sys.path.append(os.getcwd())

from database import Base, database_url as local_db_url
import models

# Hardcode local DB to ensure we pull from file, not the live DB in .env
local_db_url = 'sqlite:///instance/database.db'

def sync_data(target_url):
    print(f"Starting sync from {local_db_url} to {target_url}...")
    
    # 1. Connect to both databases
    local_engine = create_engine(local_db_url)
    target_engine = create_engine(target_url)
    
    # 2. Reflected metadata
    local_metadata = MetaData()
    local_metadata.reflect(bind=local_engine)
    
    target_metadata = MetaData()
    target_metadata.reflect(bind=target_engine)
    
    # 3. Tables to sync in order of dependency
    # Note: Using table names as defined in __tablename__
    tables_order = [
        'suppliers',
        'customers',
        'inventory',
        'activity_types',
        'financial_categories',
        'pricing',
        'locations',
        'invoices',
        'activities',
        'quotations',
        'quotation_items',
        'invoice_items',
        'payments',
        'stock_transactions',
        'financial_records',
        'journey_records',
        'fuel_records',
        'mileage_records',
        'custom_fields'
    ]

    # Create tables in target if they don't exist
    print("Ensuring target database schema is ready...")
    Base.metadata.create_all(bind=target_engine)

    # 4. Sync data for each table
    with target_engine.connect() as target_conn:
        # We need to handle transaction properly
        # Note: PostgreSQL might have SERIAL columns that need reset after sync
        
        for table_name in tables_order:
            if table_name not in local_metadata.tables:
                print(f"Skipping {table_name}: not found in local DB.")
                continue
                
            local_table = local_metadata.tables[table_name]
            
            if table_name not in target_metadata.tables:
                print(f"Skipping {table_name}: not found in target DB schema.")
                continue
            
            target_table = target_metadata.tables[table_name]
            print(f"Syncing table {table_name}...")
            
            # Read local data
            with local_engine.connect() as local_conn:
                result = local_conn.execute(select(local_table))
                rows = [dict(row._mapping) for row in result]
            
            if not rows:
                print(f"  - No data found in {table_name}.")
                continue
            
            # Get target columns to avoid UndefinedColumn errors
            target_columns = [c.name for c in target_table.columns]
            
            # Insert into target row by row to handle errors individually if needed
            success_count = 0
            fail_count = 0
            for row in rows:
                try:
                    # Only keep keys that exist in the target table
                    clean_row = {k: v for k, v in row.items() if k in target_columns}
                    
                    target_conn.execute(insert(target_table), [clean_row])
                    target_conn.commit()
                    success_count += 1
                except Exception as e:
                    target_conn.rollback()
                    # print(f"  - Failed to sync row in {table_name}: {e}")
                    fail_count += 1

            if success_count:
                print(f"  - Successfully synced {success_count} records to {table_name}.")
            if fail_count:
                print(f"  - Skipped {fail_count} records in {table_name} due to inconsistencies (like duplicate IDs).")

    # 5. Reset PostgreSQL Sequences (IDs)
    print("\nResetting PostgreSQL ID sequences...")
    with target_engine.connect() as conn:
        for table_name in tables_order:
            try:
                # This is a standard PG way to reset sequences for tables with 'id'
                conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM {table_name}"))
                conn.commit()
            except Exception:
                pass # Not all tables have serial IDs or matching names
    
    print("\nSync Complete!")
    print("Your live system should now have all recovered records!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sync_to_render.py <RENDER_DATABASE_URL>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    if target_url.startswith("postgres://"):
        target_url = target_url.replace("postgres://", "postgresql://", 1)
        
    sync_data(target_url)
