from datetime import datetime
from app import db
from sqlalchemy import Enum
import enum

class ExpenseCategory(enum.Enum):
    GENERAL_ADMIN = "General and Administration"
    OPERATIONAL = "Operational Expenses"
    MARKETING = "Marketing & Advertisement"
    COGS = "Cost of Goods"
    PAYROLL = "Employee Payroll"
    PROFESSIONAL = "Professional Services"
    TECHNOLOGY = "Technology & Software"
    RESEARCH = "Research & Development"
    MISCELLANEOUS = "Miscellaneous"
    EQUIPMENT = "Equipment"

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_date = db.Column(db.Date, nullable=False)
    category = db.Column(Enum(ExpenseCategory), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    payment_method = db.Column(db.String(50))
    reference_number = db.Column(db.String(100))
    vendor = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'expense_date': self.expense_date.isoformat() if self.expense_date else None,
            'category': self.category.value if self.category else None,
            'description': self.description,
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'reference_number': self.reference_number,
            'vendor': self.vendor,
            'notes': self.notes
        }

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # current, fixed, intangible
    category = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Numeric(12, 2), nullable=False)
    current_value = db.Column(db.Numeric(12, 2), nullable=False)
    depreciation_rate = db.Column(db.Numeric(5, 2), default=0)
    accumulated_depreciation = db.Column(db.Numeric(12, 2), default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def book_value(self):
        return float(self.current_value - self.accumulated_depreciation)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'asset_type': self.asset_type,
            'category': self.category,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'purchase_cost': float(self.purchase_cost),
            'current_value': float(self.current_value),
            'depreciation_rate': float(self.depreciation_rate),
            'accumulated_depreciation': float(self.accumulated_depreciation),
            'book_value': self.book_value,
            'notes': self.notes
        }

class Liability(db.Model):
    __tablename__ = 'liabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    liability_type = db.Column(db.String(50), nullable=False)  # current, long_term
    category = db.Column(db.String(100))
    creditor = db.Column(db.String(200))
    original_amount = db.Column(db.Numeric(12, 2), nullable=False)
    current_balance = db.Column(db.Numeric(12, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), default=0)
    due_date = db.Column(db.Date)
    payment_frequency = db.Column(db.String(50))  # monthly, quarterly, annual
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'liability_type': self.liability_type,
            'category': self.category,
            'creditor': self.creditor,
            'original_amount': float(self.original_amount),
            'current_balance': float(self.current_balance),
            'interest_rate': float(self.interest_rate),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'payment_frequency': self.payment_frequency,
            'notes': self.notes
        }

class Equity(db.Model):
    __tablename__ = 'equity'
    
    id = db.Column(db.Integer, primary_key=True)
    equity_date = db.Column(db.Date, nullable=False)
    equity_type = db.Column(db.String(100), nullable=False)  # owner_capital, retained_earnings, etc.
    description = db.Column(db.String(500))
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    transaction_type = db.Column(db.String(20))  # investment, withdrawal, profit
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'equity_date': self.equity_date.isoformat() if self.equity_date else None,
            'equity_type': self.equity_type,
            'description': self.description,
            'amount': float(self.amount),
            'transaction_type': self.transaction_type,
            'notes': self.notes
        }

class CashFlow(db.Model):
    __tablename__ = 'cash_flows'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    flow_type = db.Column(db.String(20), nullable=False)  # in or out
    category = db.Column(db.String(100))  # operating, investing, financing
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(20), default='completed')  # in_process, completed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'description': self.description,
            'flow_type': self.flow_type,
            'category': self.category,
            'amount': float(self.amount),
            'status': self.status,
            'notes': self.notes
        }

class BudgetTarget(db.Model):
    __tablename__ = 'budget_targets'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer)  # null for annual targets
    
    # Targets
    revenue_target = db.Column(db.Numeric(12, 2))
    expense_target = db.Column(db.Numeric(12, 2))
    profit_target = db.Column(db.Numeric(12, 2))
    items_sold_target = db.Column(db.Integer)
    sales_target = db.Column(db.Numeric(12, 2))
    
    # Tasks and Goals
    main_goals = db.Column(db.JSON)  # Array of {description, status, completed}
    daily_tasks = db.Column(db.JSON)  # Array of {description, status, completed}
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'month': self.month,
            'revenue_target': float(self.revenue_target) if self.revenue_target else None,
            'expense_target': float(self.expense_target) if self.expense_target else None,
            'profit_target': float(self.profit_target) if self.profit_target else None,
            'items_sold_target': self.items_sold_target,
            'sales_target': float(self.sales_target) if self.sales_target else None,
            'main_goals': self.main_goals,
            'daily_tasks': self.daily_tasks
        }

class BusinessSettings(db.Model):
    __tablename__ = 'business_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(200), nullable=False)
    business_category = db.Column(db.String(100))
    tax_id = db.Column(db.String(100))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    
    # Financial Year
    fiscal_year_start = db.Column(db.Integer, default=1)  # Month (1-12)
    
    # Capital
    starting_capital = db.Column(db.Numeric(12, 2), default=0)
    current_capital = db.Column(db.Numeric(12, 2), default=0)
    
    # Publicly Traded Settings (optional)
    is_public = db.Column(db.Boolean, default=False)
    outstanding_shares = db.Column(db.BigInteger)
    share_price = db.Column(db.Numeric(12, 4))
    
    # Settings
    default_tax_rate = db.Column(db.Numeric(5, 2), default=0)
    currency = db.Column(db.String(10), default='PHP')
    date_format = db.Column(db.String(20), default='YYYY-MM-DD')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'business_name': self.business_name,
            'business_category': self.business_category,
            'tax_id': self.tax_id,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'fiscal_year_start': self.fiscal_year_start,
            'starting_capital': float(self.starting_capital),
            'current_capital': float(self.current_capital),
            'is_public': self.is_public,
            'outstanding_shares': self.outstanding_shares,
            'share_price': float(self.share_price) if self.share_price else None,
            'default_tax_rate': float(self.default_tax_rate),
            'currency': self.currency,
            'date_format': self.date_format
        }
