"""
Sample data seeding script for demo purposes
"""
from datetime import datetime, timedelta
import random
from app import create_app, db, bcrypt
from app.models import (
    Product, Category, Customer, Sale, SaleItem, User, UserRole,
    PayrollRecord, InventoryLog, InventoryStatus
)

app = create_app()

def seed_categories():
    """Create sample categories"""
    categories = [
        {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
        {'name': 'Office Supplies', 'description': 'Office and stationery items'},
        {'name': 'Software', 'description': 'Software licenses and subscriptions'},
        {'name': 'Services', 'description': 'Professional services'},
        {'name': 'Hardware', 'description': 'Computer hardware and components'},
    ]
    
    for cat_data in categories:
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print("Categories seeded")

def seed_products():
    """Create sample products"""
    categories = {cat.name: cat.id for cat in Category.query.all()}
    
    products = [
        {'name': 'Laptop Pro 15', 'sku': 'LAP-001', 'category_id': categories.get('Electronics'), 'item_cost': 800, 'selling_price': 1200, 'current_stock': 25, 'low_stock_threshold': 5},
        {'name': 'Wireless Mouse', 'sku': 'MOU-001', 'category_id': categories.get('Electronics'), 'item_cost': 15, 'selling_price': 35, 'current_stock': 100, 'low_stock_threshold': 20},
        {'name': 'Mechanical Keyboard', 'sku': 'KEY-001', 'category_id': categories.get('Electronics'), 'item_cost': 50, 'selling_price': 120, 'current_stock': 45, 'low_stock_threshold': 10},
        {'name': '27" Monitor', 'sku': 'MON-001', 'category_id': categories.get('Electronics'), 'item_cost': 200, 'selling_price': 350, 'current_stock': 15, 'low_stock_threshold': 5},
        {'name': 'USB-C Hub', 'sku': 'HUB-001', 'category_id': categories.get('Electronics'), 'item_cost': 25, 'selling_price': 60, 'current_stock': 80, 'low_stock_threshold': 15},
        {'name': 'Office Chair', 'sku': 'CHR-001', 'category_id': categories.get('Office Supplies'), 'item_cost': 150, 'selling_price': 280, 'current_stock': 20, 'low_stock_threshold': 5},
        {'name': 'Standing Desk', 'sku': 'DSK-001', 'category_id': categories.get('Office Supplies'), 'item_cost': 300, 'selling_price': 550, 'current_stock': 8, 'low_stock_threshold': 3},
        {'name': 'Printer Paper (500)', 'sku': 'PAP-001', 'category_id': categories.get('Office Supplies'), 'item_cost': 8, 'selling_price': 15, 'current_stock': 200, 'low_stock_threshold': 50},
        {'name': 'Ink Cartridge Set', 'sku': 'INK-001', 'category_id': categories.get('Office Supplies'), 'item_cost': 40, 'selling_price': 75, 'current_stock': 60, 'low_stock_threshold': 15},
        {'name': 'Webcam HD', 'sku': 'CAM-001', 'category_id': categories.get('Electronics'), 'item_cost': 45, 'selling_price': 90, 'current_stock': 35, 'low_stock_threshold': 10},
        {'name': 'Antivirus License', 'sku': 'SOF-001', 'category_id': categories.get('Software'), 'item_cost': 20, 'selling_price': 50, 'current_stock': 999, 'is_service': False, 'track_inventory': False},
        {'name': 'IT Consultation', 'sku': 'SRV-001', 'category_id': categories.get('Services'), 'item_cost': 50, 'selling_price': 150, 'is_service': True, 'track_inventory': False, 'current_stock': 0},
        {'name': 'External SSD 1TB', 'sku': 'SSD-001', 'category_id': categories.get('Hardware'), 'item_cost': 80, 'selling_price': 150, 'current_stock': 40, 'low_stock_threshold': 10},
        {'name': 'RAM 16GB DDR4', 'sku': 'RAM-001', 'category_id': categories.get('Hardware'), 'item_cost': 45, 'selling_price': 85, 'current_stock': 30, 'low_stock_threshold': 8},
        {'name': 'Headset Pro', 'sku': 'HDS-001', 'category_id': categories.get('Electronics'), 'item_cost': 60, 'selling_price': 130, 'current_stock': 3, 'low_stock_threshold': 10},  # Low stock
    ]
    
    for prod_data in products:
        existing = Product.query.filter_by(sku=prod_data['sku']).first()
        if not existing:
            product = Product(**prod_data)
            db.session.add(product)
    
    db.session.commit()
    print("Products seeded")

def seed_customers():
    """Create sample customers"""
    customers = [
        {'name': 'Tech Solutions Inc.', 'email': 'orders@techsolutions.com', 'phone': '555-0101', 'address': '123 Tech Street, Silicon Valley, CA'},
        {'name': 'Global Corp', 'email': 'purchasing@globalcorp.com', 'phone': '555-0102', 'address': '456 Business Ave, New York, NY'},
        {'name': 'StartUp Labs', 'email': 'finance@startuplabs.io', 'phone': '555-0103', 'address': '789 Innovation Blvd, Austin, TX'},
        {'name': 'Digital Agency Pro', 'email': 'admin@digitalagency.com', 'phone': '555-0104', 'address': '321 Creative Lane, Los Angeles, CA'},
        {'name': 'Enterprise Systems', 'email': 'orders@enterprise-sys.com', 'phone': '555-0105', 'address': '654 Corporate Park, Chicago, IL'},
    ]
    
    for cust_data in customers:
        existing = Customer.query.filter_by(email=cust_data['email']).first()
        if not existing:
            customer = Customer(**cust_data)
            db.session.add(customer)
    
    db.session.commit()
    print("Customers seeded")

def seed_employee_users():
    """Create sample employee users for payroll"""
    employees = [
        {'username': 'emp_john', 'email': 'john.smith@kdrt.com', 'first_name': 'John', 'last_name': 'Smith', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 75, 'department': 'Engineering'},
        {'username': 'emp_sarah', 'email': 'sarah.johnson@kdrt.com', 'first_name': 'Sarah', 'last_name': 'Johnson', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 55, 'department': 'Sales'},
        {'username': 'emp_michael', 'email': 'michael.brown@kdrt.com', 'first_name': 'Michael', 'last_name': 'Brown', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 50, 'department': 'Engineering'},
        {'username': 'emp_emily', 'email': 'emily.davis@kdrt.com', 'first_name': 'Emily', 'last_name': 'Davis', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 45, 'department': 'Marketing'},
        {'username': 'emp_david', 'email': 'david.wilson@kdrt.com', 'first_name': 'David', 'last_name': 'Wilson', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 40, 'department': 'Operations'},
    ]
    
    for emp_data in employees:
        existing = User.query.filter_by(username=emp_data['username']).first()
        if not existing:
            password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
            user = User(
                username=emp_data['username'],
                email=emp_data['email'],
                password_hash=password_hash,
                first_name=emp_data['first_name'],
                last_name=emp_data['last_name'],
                role=emp_data['role'],
                hourly_rate=emp_data['hourly_rate'],
                department=emp_data['department'],
                is_active=True
            )
            db.session.add(user)
    
    db.session.commit()
    print("Employee users seeded")

def seed_sales():
    """Create sample sales with items"""
    customers = Customer.query.all()
    products = Product.query.filter(Product.is_service == False).all()
    
    if not customers or not products:
        print("Need customers and products first")
        return
    
    # Check if sales already exist
    if Sale.query.count() > 10:
        print("Sales already seeded")
        return
    
    # Create sales for the last 30 days
    for i in range(50):
        sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
        customer = random.choice(customers) if random.random() > 0.3 else None  # 30% walk-in
        
        # Calculate totals first
        num_items = random.randint(1, 5)
        subtotal = 0.0
        
        # Calculate subtotal
        selected_products = []
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            unit_price = float(product.selling_price)
            line_total = quantity * unit_price
            subtotal += line_total
            selected_products.append({
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total
            })
        
        # Calculate discounts and tax
        discount_pct = random.choice([0, 5, 10]) if random.random() > 0.7 else 0
        discount_amt = subtotal * (discount_pct / 100)
        tax_rate = 8.5
        tax_amt = (subtotal - discount_amt) * (tax_rate / 100)
        total = subtotal - discount_amt + tax_amt
        
        sale = Sale(
            customer_id=customer.id if customer else None,
            payment_status='paid',
            invoice_number=f'INV-{2024}{str(i+1).zfill(5)}',
            sale_date=sale_date,
            subtotal=subtotal,
            discount_percentage=discount_pct,
            discount_amount=discount_amt,
            tax_rate=tax_rate,
            tax_amount=tax_amt,
            total_amount=total,
            amount_paid=total
        )
        db.session.add(sale)
        db.session.flush()
        
        # Add sale items
        for item_data in selected_products:
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item_data['product'].id,
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                discount_percentage=0,
                line_total=item_data['line_total']
            )
            db.session.add(sale_item)
    
    db.session.commit()
    print("Sales seeded")

def seed_payroll():
    """Create sample payroll records"""
    # Get employee users (non-admin)
    employees = User.query.filter(User.role != UserRole.ADMIN).all()
    
    if not employees:
        print("Need employee users first")
        return
    
    # Check if payroll already exists
    if PayrollRecord.query.count() > 5:
        print("Payroll already seeded")
        return
    
    # Create payroll for last 2 months
    for month_offset in range(2):
        month_start = datetime.now().replace(day=1) - timedelta(days=30 * month_offset)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        for employee in employees:
            existing = PayrollRecord.query.filter_by(
                employee_id=employee.id,
                pay_period_start=month_start.date()
            ).first()
            
            if existing:
                continue
            
            hours = random.randint(140, 180)
            overtime = random.randint(0, 20)
            rate = float(employee.hourly_rate) if employee.hourly_rate else 50
            
            regular_pay = hours * rate
            overtime_pay = overtime * rate * 1.5
            bonus = random.choice([0, 0, 500]) if month_offset == 0 else 0
            gross = regular_pay + overtime_pay + bonus
            deductions = gross * 0.15  # 15% deductions
            net = gross - deductions
            
            record = PayrollRecord(
                employee_id=employee.id,
                pay_period_start=month_start.date(),
                pay_period_end=month_end.date(),
                regular_hours=hours,
                overtime_hours=overtime,
                hourly_rate=rate,
                overtime_rate=rate * 1.5,
                regular_pay=regular_pay,
                overtime_pay=overtime_pay,
                bonuses=bonus,
                gross_pay=gross,
                tax_deductions=deductions * 0.7,
                insurance_deductions=deductions * 0.3,
                total_deductions=deductions,
                net_pay=net,
                is_paid=month_offset > 0,  # Previous months are paid
                payment_date=month_end.date() if month_offset > 0 else None
            )
            db.session.add(record)
    
    db.session.commit()
    print("Payroll seeded")

def seed_inventory_logs():
    """Create sample inventory logs"""
    products = Product.query.filter(Product.track_inventory == True).all()
    
    if not products:
        print("Need products first")
        return
    
    # Check if already seeded
    if InventoryLog.query.count() > 5:
        print("Inventory logs already seeded")
        return
    
    for product in products[:5]:  # Just first 5 products
        # Stock in
        log_in = InventoryLog(
            product_id=product.id,
            type='in',
            quantity=random.randint(20, 50),
            notes='Initial stock purchase',
            status=InventoryStatus.COMPLETED
        )
        db.session.add(log_in)
        
        # Stock out
        log_out = InventoryLog(
            product_id=product.id,
            type='out',
            quantity=random.randint(5, 15),
            notes='Sales fulfillment',
            status=InventoryStatus.COMPLETED
        )
        db.session.add(log_out)
    
    db.session.commit()
    print("Inventory logs seeded")

def seed_all():
    """Run all seed functions"""
    with app.app_context():
        print("Seeding sample data...")
        seed_categories()
        seed_products()
        seed_customers()
        seed_employee_users()
        seed_sales()
        seed_payroll()
        seed_inventory_logs()
        print("Sample data seeding complete!")

if __name__ == '__main__':
    seed_all()
