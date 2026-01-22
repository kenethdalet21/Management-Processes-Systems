from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from app import db
from sqlalchemy import Enum
import enum

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

class UserRole(enum.Enum):
    ADMIN = "admin"
    OPERATIONS_MANAGER = "operations_manager"
    FINANCE_MANAGER = "finance_manager"
    EMPLOYEE = "employee"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Employee/Payroll related fields
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    hourly_rate = db.Column(db.Numeric(10, 2))
    monthly_salary = db.Column(db.Numeric(10, 2))
    
    # Relationships
    sales = db.relationship('Sale', backref='salesperson', lazy=True)
    payroll_records = db.relationship('PayrollRecord', backref='employee', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role.value if self.role else None,
            'is_active': self.is_active,
            'department': self.department,
            'position': self.position,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'monthly_salary': float(self.monthly_salary) if self.monthly_salary else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # Pricing
    item_cost = db.Column(db.Numeric(12, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(12, 2), default=0)
    other_costs = db.Column(db.Numeric(12, 2), default=0)
    selling_price = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Type
    is_service = db.Column(db.Boolean, default=False)
    
    # Inventory tracking
    track_inventory = db.Column(db.Boolean, default=True)
    current_stock = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_logs = db.relationship('InventoryLog', backref='product', lazy=True)
    sale_items = db.relationship('SaleItem', backref='product', lazy=True)
    
    @property
    def total_cost(self):
        return float(self.item_cost + self.tax_amount + self.other_costs)
    
    @property
    def estimated_profit(self):
        return float(self.selling_price - self.total_cost)
    
    @property
    def profit_margin(self):
        if self.selling_price > 0:
            return (self.estimated_profit / float(self.selling_price)) * 100
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'description': self.description,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'item_cost': float(self.item_cost),
            'tax_amount': float(self.tax_amount),
            'other_costs': float(self.other_costs),
            'total_cost': self.total_cost,
            'selling_price': float(self.selling_price),
            'estimated_profit': self.estimated_profit,
            'profit_margin': round(self.profit_margin, 2),
            'is_service': self.is_service,
            'track_inventory': self.track_inventory,
            'current_stock': self.current_stock,
            'low_stock_threshold': self.low_stock_threshold,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class InventoryStatus(enum.Enum):
    IN_PROCESS = "in_process"
    COMPLETED = "completed"

class InventoryLog(db.Model):
    __tablename__ = 'inventory_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    stock_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'in' or 'out'
    status = db.Column(Enum(InventoryStatus), default=InventoryStatus.IN_PROCESS)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'stock_date': self.stock_date.isoformat() if self.stock_date else None,
            'quantity': self.quantity,
            'type': self.type,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    tax_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sales = db.relationship('Sale', backref='customer', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'tax_id': self.tax_id
        }

class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Totals
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)
    discount_percentage = db.Column(db.Numeric(5, 2), default=0)
    discount_amount = db.Column(db.Numeric(12, 2), default=0)
    tax_rate = db.Column(db.Numeric(5, 2), default=0)
    tax_amount = db.Column(db.Numeric(12, 2), default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Payment
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, partial
    amount_paid = db.Column(db.Numeric(12, 2), default=0)
    
    # Metadata
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')
    
    @property
    def balance_due(self):
        return float(self.total_amount - self.amount_paid)
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'sale_date': self.sale_date.isoformat() if self.sale_date else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'salesperson': self.salesperson.to_dict() if self.salesperson else None,
            'subtotal': float(self.subtotal),
            'discount_percentage': float(self.discount_percentage),
            'discount_amount': float(self.discount_amount),
            'tax_rate': float(self.tax_rate),
            'tax_amount': float(self.tax_amount),
            'total_amount': float(self.total_amount),
            'payment_status': self.payment_status,
            'amount_paid': float(self.amount_paid),
            'balance_due': self.balance_due,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SaleItem(db.Model):
    __tablename__ = 'sale_items'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    discount_percentage = db.Column(db.Numeric(5, 2), default=0)
    line_total = db.Column(db.Numeric(12, 2), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'discount_percentage': float(self.discount_percentage),
            'line_total': float(self.line_total)
        }

class PayrollRecord(db.Model):
    __tablename__ = 'payroll_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pay_period_start = db.Column(db.Date, nullable=False)
    pay_period_end = db.Column(db.Date, nullable=False)
    
    # Work Hours
    regular_hours = db.Column(db.Numeric(8, 2), default=0)
    overtime_hours = db.Column(db.Numeric(8, 2), default=0)
    
    # Rates
    hourly_rate = db.Column(db.Numeric(10, 2))
    overtime_rate = db.Column(db.Numeric(10, 2))
    base_salary = db.Column(db.Numeric(12, 2))
    
    # Earnings
    regular_pay = db.Column(db.Numeric(12, 2), nullable=False)
    overtime_pay = db.Column(db.Numeric(12, 2), default=0)
    bonuses = db.Column(db.Numeric(12, 2), default=0)
    gross_pay = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Deductions
    tax_deductions = db.Column(db.Numeric(12, 2), default=0)
    insurance_deductions = db.Column(db.Numeric(12, 2), default=0)
    other_deductions = db.Column(db.Numeric(12, 2), default=0)
    total_deductions = db.Column(db.Numeric(12, 2), default=0)
    
    # Net Pay
    net_pay = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Payment
    payment_date = db.Column(db.Date)
    payment_method = db.Column(db.String(50))
    is_paid = db.Column(db.Boolean, default=False)
    
    # Metadata
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee': self.employee.to_dict() if self.employee else None,
            'pay_period_start': self.pay_period_start.isoformat() if self.pay_period_start else None,
            'pay_period_end': self.pay_period_end.isoformat() if self.pay_period_end else None,
            'regular_hours': float(self.regular_hours),
            'overtime_hours': float(self.overtime_hours),
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'overtime_rate': float(self.overtime_rate) if self.overtime_rate else None,
            'base_salary': float(self.base_salary) if self.base_salary else None,
            'regular_pay': float(self.regular_pay),
            'overtime_pay': float(self.overtime_pay),
            'bonuses': float(self.bonuses),
            'gross_pay': float(self.gross_pay),
            'tax_deductions': float(self.tax_deductions),
            'insurance_deductions': float(self.insurance_deductions),
            'other_deductions': float(self.other_deductions),
            'total_deductions': float(self.total_deductions),
            'net_pay': float(self.net_pay),
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'is_paid': self.is_paid,
            'notes': self.notes
        }

class TabPermission(db.Model):
    __tablename__ = 'tab_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tab_name = db.Column(db.String(50), nullable=False)  # products, inventory, sales, payroll, financial
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='tab_permissions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tab_name': self.tab_name,
            'is_locked': self.is_locked,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'role': self.user.role.value if self.user.role else None
            } if self.user else None
        }

class FileUpload(db.Model):
    """Model to track all uploaded files in the unified storage system"""
    __tablename__ = 'file_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # excel, csv, pdf, image
    file_size = db.Column(db.Integer)  # in bytes
    category = db.Column(db.String(100))  # products, sales, inventory, payroll, etc.
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)
    records_imported = db.Column(db.Integer, default=0)  # number of records imported from this file
    status = db.Column(db.String(50), default='uploaded')  # uploaded, processed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='uploaded_files')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'file_size_mb': round(self.file_size / (1024 * 1024), 2) if self.file_size else 0,
            'category': self.category,
            'uploaded_by': self.user.username if self.user else None,
            'description': self.description,
            'records_imported': self.records_imported,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }

# Import financial models to make them available from app.models
from app.models.financial import (
    ExpenseCategory, Expense, Asset, Liability, Equity, 
    CashFlow, BudgetTarget, BusinessSettings
)
