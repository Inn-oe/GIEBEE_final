import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Import database and models
from models import (db, Supplier, Customer, Inventory, Activity, ActivityType, Invoice, InvoiceItem, 
                   StockTransaction, FinancialRecord, CustomField)

# create the app
app = Flask(__name__)
# setup a secret key, required by sessions
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "solar_company_secret_key"
# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///database.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    """Dashboard showing overview of activities and key metrics"""
    # Get counts for dashboard
    suppliers_count = Supplier.query.count()
    customers_count = Customer.query.count()
    inventory_count = Inventory.query.count()
    invoices_count = Invoice.query.count()
    activities_count = Activity.query.count()
    
    return render_template('dashboard.html',
                         suppliers_count=suppliers_count,
                         customers_count=customers_count,
                         inventory_count=inventory_count,
                         invoices_count=invoices_count,
                         activities_count=activities_count)

@app.route('/suppliers')
def suppliers():
    """List all suppliers"""
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    """Add new supplier"""
    if request.method == 'POST':
        from models import Currency
        supplier = Supplier(
            name=request.form['name'],
            contact_person=request.form['contact_person'],
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address'],
            payment_terms=request.form['payment_terms'],
            currency=Currency(request.form['currency']) if request.form['currency'] else Currency.USD
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully!', 'success')
        return redirect(url_for('suppliers'))
    return render_template('add_supplier.html')

@app.route('/customers')
def customers():
    """List all customers"""
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    """Add new customer"""
    if request.method == 'POST':
        customer = Customer(
            name=request.form['name'],
            identification_number=request.form['identification_number'],
            citizenship=request.form['citizenship'],
            address=request.form['address'],
            phone=request.form['phone'],
            email=request.form['email']
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    return render_template('add_customer.html')

@app.route('/inventory')
def inventory():
    """View inventory with search and filter"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Inventory.query
    
    if search:
        query = query.filter(
            db.or_(
                Inventory.name.contains(search),
                Inventory.brand.contains(search),
                Inventory.specifications.contains(search)
            )
        )
    
    if category:
        query = query.filter(Inventory.category == category)
    
    items = query.all()
    categories = db.session.query(Inventory.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('inventory.html', items=items, categories=categories, search=search, selected_category=category)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    """Add new inventory item"""
    if request.method == 'POST':
        from models import Currency, PaymentType
        item = Inventory(
            name=request.form['name'],
            brand=request.form['brand'],
            category=request.form['category'],
            specifications=request.form['specifications'],
            quantity=int(request.form['quantity']),
            unit_price=float(request.form['unit_price']),
            currency=Currency(request.form['currency']) if request.form['currency'] else Currency.USD,
            supplier_id=int(request.form['supplier_id']) if request.form['supplier_id'] else None,
            payment_type=PaymentType(request.form['payment_type']) if request.form['payment_type'] else None
        )
        db.session.add(item)
        db.session.commit()
        
        # Record stock transaction
        from models import TransactionType
        stock_transaction = StockTransaction(
            inventory_id=item.id,
            transaction_type=TransactionType.STOCK_IN,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_value=item.quantity * item.unit_price,
            notes=f'Initial stock for {item.name}'
        )
        db.session.add(stock_transaction)
        db.session.commit()
        
        flash('Inventory item added successfully!', 'success')
        return redirect(url_for('inventory'))
    suppliers = Supplier.query.all()
    return render_template('add_inventory.html', suppliers=suppliers)

@app.route('/invoices')
def invoices():
    """List all invoices"""
    invoices = Invoice.query.order_by(Invoice.date_created.desc()).all()
    return render_template('invoices.html', invoices=invoices)

@app.route('/invoices/add', methods=['GET', 'POST'])
def add_invoice():
    """Create new invoice"""
    if request.method == 'POST':
        from models import InvoiceStatus, TransactionType
        
        # Begin transaction
        try:
            # Process and validate invoice items first
            item_ids = request.form.getlist('item_id[]')
            quantities = request.form.getlist('quantity[]')
            unit_prices = request.form.getlist('unit_price[]')
            
            calculated_total = 0
            invoice_items_data = []
            
            # Validate all items and calculate total
            for i, item_id in enumerate(item_ids):
                if item_id:
                    inventory_item = Inventory.query.get(int(item_id))
                    if not inventory_item:
                        flash(f'Item not found', 'error')
                        return redirect(url_for('add_invoice'))
                    
                    qty = int(quantities[i])
                    if inventory_item.quantity < qty:
                        flash(f'Insufficient stock for {inventory_item.name}. Available: {inventory_item.quantity}', 'error')
                        return redirect(url_for('add_invoice'))
                    
                    unit_price = float(unit_prices[i])
                    item_total = qty * unit_price
                    calculated_total += item_total
                    
                    invoice_items_data.append({
                        'inventory_id': int(item_id),
                        'inventory_item': inventory_item,
                        'quantity': qty,
                        'unit_price': unit_price,
                        'item_total': item_total
                    })
            
            # Create invoice with calculated total
            from models import InvoiceStatus, Currency, PaymentType
            invoice = Invoice(
                customer_id=int(request.form['customer_id']),
                total_amount=calculated_total,
                currency=Currency(request.form['currency']) if request.form['currency'] else Currency.USD,
                status=InvoiceStatus.PENDING
            )
            db.session.add(invoice)
            db.session.flush()  # Get invoice ID without committing
            
            # Create invoice items and update stock
            for item_data in invoice_items_data:
                invoice_item = InvoiceItem(
                    invoice_id=invoice.id,
                    inventory_id=item_data['inventory_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price']
                )
                db.session.add(invoice_item)
                
                # Update inventory quantity
                item_data['inventory_item'].quantity -= item_data['quantity']
                
                # Record stock transaction
                stock_transaction = StockTransaction(
                    inventory_id=item_data['inventory_id'],
                    transaction_type=TransactionType.STOCK_OUT,
                    quantity=-item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    total_value=-item_data['item_total'],
                    reference_id=invoice.id,
                    reference_type='INVOICE',
                    notes=f'Sold via invoice #{invoice.id}'
                )
                db.session.add(stock_transaction)
            
            # Commit all changes
            db.session.commit()
            flash('Invoice created successfully!', 'success')
            return redirect(url_for('invoices'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating invoice: {str(e)}', 'error')
            return redirect(url_for('add_invoice'))
    
    customers = Customer.query.all()
    inventory_items = Inventory.query.filter(Inventory.quantity > 0).all()
    return render_template('add_invoice.html', customers=customers, inventory_items=inventory_items)

@app.route('/financial')
def financial():
    """Financial dashboard"""
    # Calculate totals
    from models import FinancialType
    total_sales = db.session.query(db.func.sum(Invoice.total_amount)).scalar() or 0
    total_expenses = db.session.query(db.func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == FinancialType.EXPENSE
    ).scalar() or 0
    total_income = db.session.query(db.func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == FinancialType.INCOME
    ).scalar() or 0
    
    profit = (total_sales + total_income) - total_expenses
    
    recent_transactions = FinancialRecord.query.order_by(
        FinancialRecord.date.desc()
    ).limit(10).all()
    
    return render_template('financial.html', 
                         total_sales=total_sales,
                         total_expenses=total_expenses, 
                         total_income=total_income,
                         profit=profit,
                         recent_transactions=recent_transactions)

@app.route('/financial/add', methods=['GET', 'POST'])
def add_financial_record():
    """Add financial record"""
    if request.method == 'POST':
        from models import FinancialType
        record = FinancialRecord(
            type=FinancialType(request.form['type']),
            category=request.form['category'],
            description=request.form['description'],
            amount=float(request.form['amount']),
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        )
        db.session.add(record)
        db.session.commit()
        flash('Financial record added successfully!', 'success')
        return redirect(url_for('financial'))
    return render_template('add_financial_record.html')

@app.route('/activities')
def activities():
    """List company activities"""
    activities = Activity.query.order_by(Activity.date.desc()).all()
    return render_template('activities.html', activities=activities)

@app.route('/activities/add', methods=['GET', 'POST'])
def add_activity():
    """Add new activity"""
    if request.method == 'POST':
        from models import ActivityStatusEnum, Currency
        activity = Activity(
            customer_id=int(request.form['customer_id']),
            activity_type_id=int(request.form['activity_type_id']),
            description=request.form['description'],
            status=ActivityStatusEnum(request.form['status']),
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            currency=Currency.USD
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity added successfully!', 'success')
        return redirect(url_for('activities'))
    
    customers = Customer.query.all()
    activity_types = ActivityType.query.filter_by(is_active=True).all()
    return render_template('add_activity.html', customers=customers, activity_types=activity_types)

@app.route('/invoice/<int:invoice_id>/pdf')
def generate_invoice_pdf(invoice_id):
    """Generate PDF invoice"""
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice_items = InvoiceItem.query.filter_by(invoice_id=invoice_id).all()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Invoice header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, f"INVOICE #{invoice.id}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Date: {invoice.date_created.strftime('%Y-%m-%d')}")
    p.drawString(50, 700, f"Customer: {invoice.customer_name}")
    p.drawString(50, 680, f"Address: {invoice.customer_address}")
    
    # Invoice items
    y_position = 640
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y_position, "Item")
    p.drawString(200, y_position, "Quantity")
    p.drawString(300, y_position, "Unit Price")
    p.drawString(400, y_position, "Total")
    
    y_position -= 20
    p.setFont("Helvetica", 10)
    
    for item in invoice_items:
        inventory = Inventory.query.get(item.inventory_id)
        if inventory:
            p.drawString(50, y_position, f"{inventory.name} - {inventory.brand}")
        p.drawString(200, y_position, str(item.quantity))
        p.drawString(300, y_position, f"R{item.unit_price:.2f}")
        p.drawString(400, y_position, f"R{item.quantity * item.unit_price:.2f}")
        y_position -= 15
    
    # Total
    y_position -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(300, y_position, f"TOTAL: R{invoice.total_amount:.2f}")
    
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'invoice_{invoice.id}.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)