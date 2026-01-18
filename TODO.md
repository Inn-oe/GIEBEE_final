# TODO List for Fixing Database Connection Error and Missing Routes

- [x] Modify database.py to create the 'instance' directory if it doesn't exist before initializing the database engine.
- [x] Test the fix by running `python main.py` to ensure the app starts without the database error.
- [x] Add missing routes to main.py (suppliers, customers, inventory, quotations, activities, financial, fuel_tracking, mileage_tracking, journey_tracking, locations, pricing).
- [x] Add missing "add" routes (add_supplier, add_customer, add_inventory, add_quotation, add_activity, add_financial_record).
- [x] Test the application to ensure all sidebar links work without BuildError.
- [x] Enable adding custom item names not already in stock when creating quotations in the quotations tab.
