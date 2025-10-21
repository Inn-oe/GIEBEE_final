from database import db_session, init_db, engine
from models import StockTransaction, TransactionType, FinancialRecord, FinancialType, FinancialCategory
from sqlalchemy import text
import os

# Check database type
database_url = os.environ.get('DATABASE_URL', '').lower()
is_mysql = 'mysql' in database_url
is_postgresql = 'postgresql' in database_url

if is_mysql:
    # For MySQL migration
    try:
        with engine.connect() as conn:
            # Execute schema.sql for MySQL
            with open('schema.sql', 'r') as f:
                schema_sql = f.read()

            # Split into individual statements and execute
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            for stmt in statements:
                if stmt:
                    conn.execute(text(stmt))
            conn.commit()
        print('MySQL schema migration completed successfully')
    except Exception as e:
        print(f'Error during MySQL migration: {e}')
elif is_postgresql:
    # For PostgreSQL migration - use SQLAlchemy to create tables
    try:
        init_db()
        print('PostgreSQL schema migration completed successfully using SQLAlchemy')
    except Exception as e:
        print(f'Error during PostgreSQL migration: {e}')
else:
    # Original SQLite migration
    init_db()

try:
    # Use raw SQL to update the database directly
    with engine.connect() as conn:
        # Update string values to enum values for stock_transactions
        conn.execute(text("UPDATE stock_transactions SET transaction_type = 'STOCK_IN' WHERE transaction_type = 'Stock In'"))
        conn.execute(text("UPDATE stock_transactions SET transaction_type = 'STOCK_OUT' WHERE transaction_type = 'Stock Out'"))
        conn.execute(text("UPDATE stock_transactions SET transaction_type = 'ADJUSTMENT' WHERE transaction_type = 'Adjustment'"))

        # Update string values to enum values for financial_records
        conn.execute(text("UPDATE financial_records SET type = 'INCOME' WHERE type = 'Income'"))
        conn.execute(text("UPDATE financial_records SET type = 'EXPENSE' WHERE type = 'Expense'"))

        # Update string values to enum values for financial_categories
        conn.execute(text("UPDATE financial_categories SET type = 'INCOME' WHERE type = 'Income'"))
        conn.execute(text("UPDATE financial_categories SET type = 'EXPENSE' WHERE type = 'Expense'"))

        conn.commit()
    print('Migration completed successfully using raw SQL')
except Exception as e:
    print(f'Error during migration: {e}')
