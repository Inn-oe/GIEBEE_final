# Models for Solar Company Management System
# Referenced from blueprint:python_database integration

from datetime import datetime
from sqlalchemy import Enum
import enum

# Create db instance to be imported in main.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class PaymentType(enum.Enum):
    CASH = "Cash"
    ECOCASH = "EcoCash"
    SWIPE = "Swipe"
    TRANSFER = "Transfer"
    CREDIT = "Credit"

class Currency(enum.Enum):
    USD = "USD"
    ZWL = "ZWL"
    RAND = "RAND"

class StockChangeReason(enum.Enum):
    SOLD_TO_CUSTOMER = "Sold to Customer"
    INSTALLED_TO_CLIENT = "Installed to Client"
    DAMAGED = "Damaged"
    RETURNED = "Returned"
    ADJUSTMENT = "Stock Adjustment"

class ExpenseCategory(enum.Enum):
    FUEL = "Fuel"
    CAR_MAINTENANCE = "Car Maintenance"
    RENT = "Rent"
    SOLAR_MAINTENANCE = "Solar Maintenance"
    SERVICES = "Services"
    EMPLOYEE_PAYMENTS = "Employee Payments"
    UTILITIES = "Utilities"
    EQUIPMENT = "Equipment Purchase"
    OTHER = "Other Expenses"

class ActivityStatusEnum(enum.Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class quotationstatus(enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    OVERDUE = "Overdue"
    CANCELLED = "Cancelled"

class TransactionType(enum.Enum):
    STOCK_IN = "Stock In"
    STOCK_OUT = "Stock Out"
    ADJUSTMENT = "Adjustment"

class FinancialType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class Supplier(db.Model):
    """Suppliers who provide inventory to Giebee Engineering"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    payment_terms = db.Column(db.String(100))
    currency = db.Column(Enum(Currency), default=Currency.USD)
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory_items = db.relationship("Inventory", back_populates="supplier")
    
    def __repr__(self):
        return f'<Supplier {self.name}>'

class Customer(db.Model):
    """Customers who purchase from Giebee Engineering"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    identification_number = db.Column(db.String(50))
    citizenship = db.Column(db.String(100))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quotations = db.relationship("quotation", back_populates="customer")
    activities = db.relationship("Activity", back_populates="customer")
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Inventory(db.Model):
    """Inventory items with enhanced tracking for Giebee Engineering"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(100))  # Solar Panel, Battery, CCTV, Geyser, Alarm, etc.
    specifications = db.Column(db.Text)  # e.g., "24v 100ah", "48v 100ah", "5MP Camera", etc.
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, nullable=False)
    currency = db.Column(Enum(Currency), default=Currency.USD)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    payment_type = db.Column(Enum(PaymentType))
    minimum_stock_level = db.Column(db.Integer, default=5)
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = db.relationship("Supplier", back_populates="inventory_items")
    quotation_items = db.relationship("quotationItem", back_populates="inventory")
    stock_transactions = db.relationship("StockTransaction", back_populates="inventory")
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_stock_level
    
    @property
    def total_value(self):
        return self.quantity * self.unit_price
    
    def __repr__(self):
        return f'<Inventory {self.name} - {self.brand}>'

class ActivityType(db.Model):
    """Custom activity types for Giebee Engineering"""
    __tablename__ = 'activity_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    activities = db.relationship("Activity", back_populates="activity_type_ref")
    
    def __repr__(self):
        return f'<ActivityType {self.name}>'

class Activity(db.Model):
    """Activities performed by Giebee Engineering for customers"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    activity_type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(Enum(ActivityStatusEnum), default=ActivityStatusEnum.SCHEDULED)
    date = db.Column(db.Date, nullable=False)
    completed_date = db.Column(db.Date)
    technician = db.Column(db.String(100))
    equipment_used = db.Column(db.Text)  # List of equipment/inventory used
    labor_hours = db.Column(db.Float)
    labor_cost = db.Column(db.Float)
    material_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)
    currency = db.Column(Enum(Currency), default=Currency.USD)
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = db.relationship("Customer", back_populates="activities")
    activity_type_ref = db.relationship("ActivityType", back_populates="activities")
    
    def __repr__(self):
        return f'<Activity {self.activity_type_ref.name if self.activity_type_ref else "N/A"} for {self.customer.name if self.customer else "N/A"}>'

class quotation(db.Model):
    """quotations for Giebee Engineering services and sales"""
    __tablename__ = 'quotations'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(Enum(Currency), default=Currency.USD)
    tax_amount = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    status = db.Column(Enum(quotationstatus), default=quotationstatus.PENDING)
    due_date = db.Column(db.Date)
    paid_date = db.Column(db.Date)
    payment_method = db.Column(Enum(PaymentType))
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = db.relationship("Customer", back_populates="quotations")
    quotation_items = db.relationship("quotationItem", back_populates="quotation", cascade="all, delete-orphan")
    
    @property
    def final_amount(self):
        return self.total_amount + self.tax_amount - self.discount_amount
    
    def __repr__(self):
        return f'<quotation #{self.id} - {self.customer.name if self.customer else "N/A"}>'

class quotationItem(db.Model):
    """Items on an quotation"""
    __tablename__ = 'quotation_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)  # Additional description if needed
    
    # Relationships
    quotation = db.relationship("quotation", back_populates="quotation_items")
    inventory = db.relationship("Inventory", back_populates="quotation_items")
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price
    
    def __repr__(self):
        return f'<quotationItem {self.quantity}x {self.inventory.name}>'

class StockTransaction(db.Model):
    """Track all stock movements (in, out, adjustments) with reasons"""
    __tablename__ = 'stock_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    transaction_type = db.Column(Enum(TransactionType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Positive for in, negative for out
    unit_price = db.Column(db.Float)
    total_value = db.Column(db.Float)
    currency = db.Column(Enum(Currency), default=Currency.USD)
    reason = db.Column(Enum(StockChangeReason))  # Reason for stock change
    reference_id = db.Column(db.Integer)  # Reference to quotation, purchase order, etc.
    reference_type = db.Column(db.String(50))  # "quotation", "PURCHASE", "ADJUSTMENT", etc.
    customer_name = db.Column(db.String(200))  # For tracking who items were sold/installed to
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory = db.relationship("Inventory", back_populates="stock_transactions")
    
    def __repr__(self):
        return f'<StockTransaction {self.transaction_type.value}: {self.quantity}x {self.inventory.name if self.inventory else "N/A"}>'

class FinancialRecord(db.Model):
    """Track all financial transactions for Giebee Engineering"""
    __tablename__ = 'financial_records'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(Enum(FinancialType), nullable=False)
    category = db.Column(db.String(100))  # Using ExpenseCategory enum values
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(Enum(Currency), default=Currency.USD)
    date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(Enum(PaymentType))
    receipt_number = db.Column(db.String(100))
    vendor_supplier = db.Column(db.String(200))
    reference_id = db.Column(db.Integer)  # Link to quotations, activities, etc.
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<FinancialRecord {self.type.value}: {self.currency.value if self.currency else "USD"}{self.amount}>'

class CustomField(db.Model):
    """Dynamic custom fields for inventory and other entities"""
    __tablename__ = 'custom_fields'
    
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # "inventory", "company", etc.
    entity_id = db.Column(db.Integer, nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    field_value = db.Column(db.Text)
    field_type = db.Column(db.String(20), default='text')  # text, number, date, boolean
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CustomField {self.field_name}: {self.field_value}>'