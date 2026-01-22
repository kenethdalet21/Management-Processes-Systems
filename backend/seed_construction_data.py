"""
Construction industry sample data seeding script
"""
from datetime import datetime, timedelta
import random
from app import create_app, db, bcrypt
from app.models import (
    Product, Category, Customer, Sale, SaleItem, User, UserRole,
    PayrollRecord, InventoryLog, InventoryStatus
)

app = create_app()

def clear_existing_data():
    """Clear existing data"""
    with app.app_context():
        SaleItem.query.delete()
        Sale.query.delete()
        InventoryLog.query.delete()
        PayrollRecord.query.delete()
        Product.query.delete()
        Category.query.delete()
        Customer.query.delete()
        # Keep default users
        db.session.commit()
        print("Existing data cleared")

def seed_categories():
    """Create construction industry categories"""
    categories = [
        {'name': 'Building Materials', 'description': 'Cement, concrete, blocks, bricks'},
        {'name': 'Steel & Metals', 'description': 'Reinforcement bars, steel beams, metal sheets'},
        {'name': 'Wood & Timber', 'description': 'Lumber, plywood, wooden beams'},
        {'name': 'Construction Services', 'description': 'Labor, consulting, project management'},
        {'name': 'Tools & Equipment', 'description': 'Construction tools and heavy equipment rental'},
    ]
    
    for cat_data in categories:
        category = Category(**cat_data)
        db.session.add(category)
    
    db.session.commit()
    print("Categories seeded")

def seed_products():
    """Create construction materials and services"""
    categories = {cat.name: cat.id for cat in Category.query.all()}
    
    products = [
        # Building Materials
        {'name': 'Portland Cement 50kg', 'sku': 'CEM-001', 'category_id': categories.get('Building Materials'), 'item_cost': 180, 'selling_price': 250, 'current_stock': 500, 'low_stock_threshold': 100, 'track_inventory': True},
        {'name': 'Concrete Hollow Blocks', 'sku': 'BLK-001', 'category_id': categories.get('Building Materials'), 'item_cost': 12, 'selling_price': 18, 'current_stock': 2000, 'low_stock_threshold': 500, 'track_inventory': True},
        {'name': 'Ready Mix Concrete m³', 'sku': 'RMC-001', 'category_id': categories.get('Building Materials'), 'item_cost': 3500, 'selling_price': 4800, 'current_stock': 50, 'low_stock_threshold': 10, 'track_inventory': True},
        {'name': 'Gravel & Sand m³', 'sku': 'GRV-001', 'category_id': categories.get('Building Materials'), 'item_cost': 800, 'selling_price': 1200, 'current_stock': 80, 'low_stock_threshold': 20, 'track_inventory': True},
        
        # Steel & Metals
        {'name': 'Rebar 10mm x 6m', 'sku': 'REB-010', 'category_id': categories.get('Steel & Metals'), 'item_cost': 180, 'selling_price': 280, 'current_stock': 800, 'low_stock_threshold': 200, 'track_inventory': True},
        {'name': 'Rebar 12mm x 6m', 'sku': 'REB-012', 'category_id': categories.get('Steel & Metals'), 'item_cost': 250, 'selling_price': 380, 'current_stock': 600, 'low_stock_threshold': 150, 'track_inventory': True},
        {'name': 'Steel I-Beam per meter', 'sku': 'STL-001', 'category_id': categories.get('Steel & Metals'), 'item_cost': 1200, 'selling_price': 1800, 'current_stock': 100, 'low_stock_threshold': 25, 'track_inventory': True},
        {'name': 'Corrugated Steel Sheet', 'sku': 'COR-001', 'category_id': categories.get('Steel & Metals'), 'item_cost': 350, 'selling_price': 520, 'current_stock': 150, 'low_stock_threshold': 30, 'track_inventory': True},
        
        # Wood & Timber
        {'name': 'Marine Plywood 4x8', 'sku': 'PLY-001', 'category_id': categories.get('Wood & Timber'), 'item_cost': 800, 'selling_price': 1200, 'current_stock': 150, 'low_stock_threshold': 30, 'track_inventory': True},
        {'name': '2x4 Lumber per piece', 'sku': 'LUM-001', 'category_id': categories.get('Wood & Timber'), 'item_cost': 120, 'selling_price': 180, 'current_stock': 400, 'low_stock_threshold': 100, 'track_inventory': True},
        {'name': 'Hardwood Flooring sqm', 'sku': 'FLR-001', 'category_id': categories.get('Wood & Timber'), 'item_cost': 450, 'selling_price': 680, 'current_stock': 200, 'low_stock_threshold': 50, 'track_inventory': True},
        
        # Tools & Equipment
        {'name': 'Power Drill Industrial', 'sku': 'DRL-001', 'category_id': categories.get('Tools & Equipment'), 'item_cost': 3500, 'selling_price': 5200, 'current_stock': 25, 'low_stock_threshold': 5, 'track_inventory': True},
        {'name': 'Welding Machine 200A', 'sku': 'WLD-001', 'category_id': categories.get('Tools & Equipment'), 'item_cost': 15000, 'selling_price': 22000, 'current_stock': 10, 'low_stock_threshold': 2, 'track_inventory': True},
        {'name': 'Concrete Mixer 1-Bag', 'sku': 'MIX-001', 'category_id': categories.get('Tools & Equipment'), 'item_cost': 25000, 'selling_price': 35000, 'current_stock': 8, 'low_stock_threshold': 2, 'track_inventory': True},
        {'name': 'Scaffolding Set', 'sku': 'SCF-001', 'category_id': categories.get('Tools & Equipment'), 'item_cost': 8000, 'selling_price': 12000, 'current_stock': 5, 'low_stock_threshold': 3, 'track_inventory': True},
        
        # Services
        {'name': 'Project Management Service', 'sku': 'SRV-001', 'category_id': categories.get('Construction Services'), 'item_cost': 0, 'selling_price': 50000, 'is_service': True, 'track_inventory': False, 'current_stock': 0},
        {'name': 'Site Engineering Service', 'sku': 'SRV-002', 'category_id': categories.get('Construction Services'), 'item_cost': 0, 'selling_price': 35000, 'is_service': True, 'track_inventory': False, 'current_stock': 0},
    ]
    
    for prod_data in products:
        product = Product(**prod_data)
        db.session.add(product)
    
    db.session.commit()
    print("Products seeded")

def seed_customers():
    """Create construction company customers"""
    customers = [
        {'name': 'Mega Build Construction Corp', 'email': 'projects@megabuild.com', 'phone': '+63-917-123-4567', 'address': '123 Builders Ave, Quezon City, Metro Manila'},
        {'name': 'Skyline Developers Inc', 'email': 'procurement@skyline.com', 'phone': '+63-918-234-5678', 'address': '456 Construction Blvd, Makati City, Metro Manila'},
        {'name': 'Prime Infrastructure Solutions', 'email': 'supply@primeinfra.com', 'phone': '+63-919-345-6789', 'address': '789 Engineering Park, Taguig City, Metro Manila'},
        {'name': 'Urban Builders Group', 'email': 'materials@urbanbuilders.com', 'phone': '+63-920-456-7890', 'address': '321 Development Road, Pasig City, Metro Manila'},
        {'name': 'Coastal Construction & Realty', 'email': 'orders@coastalcr.com', 'phone': '+63-921-567-8901', 'address': '654 Contractor Street, Mandaluyong City, Metro Manila'},
    ]
    
    for cust_data in customers:
        customer = Customer(**cust_data)
        db.session.add(customer)
    
    db.session.commit()
    print("Customers seeded")

def seed_employee_users():
    """Create construction company employees"""
    employees = [
        {'username': 'eng_carlos', 'email': 'carlos.santos@kdrt.com', 'first_name': 'Carlos', 'last_name': 'Santos', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 85, 'department': 'Civil Engineering'},
        {'username': 'eng_maria', 'email': 'maria.cruz@kdrt.com', 'first_name': 'Maria', 'last_name': 'Cruz', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 75, 'department': 'Structural Engineering'},
        {'username': 'sup_juan', 'email': 'juan.reyes@kdrt.com', 'first_name': 'Juan', 'last_name': 'Reyes', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 65, 'department': 'Site Supervision'},
        {'username': 'est_anna', 'email': 'anna.garcia@kdrt.com', 'first_name': 'Anna', 'last_name': 'Garcia', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 70, 'department': 'Cost Estimation'},
        {'username': 'pm_pedro', 'email': 'pedro.villa@kdrt.com', 'first_name': 'Pedro', 'last_name': 'Villa', 'role': UserRole.OPERATIONS_MANAGER, 'hourly_rate': 90, 'department': 'Project Management'},
    ]
    
    for emp_data in employees:
        # Check if user already exists
        existing_user = User.query.filter_by(email=emp_data['email']).first()
        if existing_user:
            print(f"User {emp_data['email']} already exists, skipping...")
            continue
            
        password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(
            username=emp_data['username'],
            email=emp_data['email'],
            password_hash=password_hash,
            first_name=emp_data['first_name'],
            last_name=emp_data['last_name'],
            role=emp_data['role'],
            hourly_rate=emp_data['hourly_rate'],
            department=emp_data['department']
        )
        db.session.add(user)
    
    db.session.commit()
    print("Employee users seeded")

def seed_sales():
    """Create sample construction sales transactions"""
    products = Product.query.all()
    customers = Customer.query.all()
    
    if not products or not customers:
        print("Please seed products and customers first")
        return
    
    # Check if sales already exist
    existing_sales = Sale.query.count()
    if existing_sales > 0:
        print("Sales already seeded")
        return
    
    # Generate 50 sales over the last 30 days
    for i in range(50):
        sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
        customer = random.choice(customers)
        
        # Add 1-5 items per sale
        num_items = random.randint(1, 5)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        subtotal = 0
        sale_items = []
        
        for product in selected_products:
            quantity = random.randint(1, 20)
            unit_price = product.selling_price
            line_total = quantity * unit_price
            subtotal += line_total
            
            sale_item = SaleItem(
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                discount_percentage=0,
                line_total=line_total
            )
            sale_items.append(sale_item)
        
        sale = Sale(
            customer_id=customer.id,
            invoice_number=f'INV-2024{str(i+1).zfill(5)}',
            sale_date=sale_date,
            subtotal=subtotal,
            total_amount=subtotal,
            payment_status='paid' if random.random() > 0.1 else 'pending'
        )
        sale.items = sale_items
        
        db.session.add(sale)
    
    db.session.commit()
    print("Sales seeded")

def seed_payroll():
    """Create sample payroll records for construction employees"""
    employees = User.query.filter(User.role != UserRole.ADMIN).all()
    
    if not employees:
        print("Please seed employee users first")
        return
    
    # Check if payroll already exists
    existing_payroll = PayrollRecord.query.count()
    if existing_payroll > 0:
        print("Payroll already seeded")
        return
    
    # Generate payroll for last 2 pay periods
    for employee in employees:
        # Skip if hourly_rate is not set
        if not employee.hourly_rate:
            continue
            
        for i in range(2):
            period_end = datetime.now() - timedelta(days=15 * i)
            period_start = period_end - timedelta(days=14)
            
            regular_hours = random.randint(80, 176)  # 40-88 hours per week * 2 weeks
            overtime_hours = random.randint(0, 20)
            bonuses = random.randint(0, 5000)
            
            regular_pay = regular_hours * float(employee.hourly_rate)
            overtime_pay = overtime_hours * float(employee.hourly_rate) * 1.5
            gross_pay = regular_pay + overtime_pay + bonuses
            
            tax_deductions = gross_pay * 0.1
            insurance_deductions = random.randint(500, 1000)
            other_deductions = random.randint(200, 500)
            total_deductions = tax_deductions + insurance_deductions + other_deductions
            
            net_pay = gross_pay - total_deductions
            
            payroll = PayrollRecord(
                employee_id=employee.id,
                pay_period_start=period_start.date(),
                pay_period_end=period_end.date(),
                regular_hours=regular_hours,
                overtime_hours=overtime_hours,
                hourly_rate=employee.hourly_rate,
                overtime_rate=float(employee.hourly_rate) * 1.5,
                regular_pay=regular_pay,
                overtime_pay=overtime_pay,
                bonuses=bonuses,
                gross_pay=gross_pay,
                tax_deductions=tax_deductions,
                insurance_deductions=insurance_deductions,
                other_deductions=other_deductions,
                total_deductions=total_deductions,
                net_pay=net_pay,
                payment_date=period_end.date(),
                payment_method='Bank Transfer',
                is_paid=True,
                notes=f'Pay period for {employee.department}'
            )
            db.session.add(payroll)
    
    db.session.commit()
    print("Payroll seeded")

def seed_inventory_logs():
    """Create sample inventory logs"""
    products = Product.query.filter_by(track_inventory=True).all()
    
    if not products:
        print("Please seed products first")
        return
    
    # Check if inventory logs already exist
    existing_logs = InventoryLog.query.count()
    if existing_logs > 0:
        print("Inventory logs already seeded")
        return
    
    # Create some inventory movements
    for product in products[:10]:  # First 10 products
        # Stock in
        for _ in range(random.randint(2, 5)):
            log_date = datetime.now() - timedelta(days=random.randint(1, 60))
            quantity = random.randint(50, 200)
            
            log = InventoryLog(
                product_id=product.id,
                type='in',
                quantity=quantity,
                stock_date=log_date,
                status=InventoryStatus.COMPLETED,
                notes=f'Supplier delivery - PO-{random.randint(1000, 9999)}'
            )
            db.session.add(log)
        
        # Stock out
        for _ in range(random.randint(1, 3)):
            log_date = datetime.now() - timedelta(days=random.randint(1, 30))
            quantity = random.randint(10, 50)
            
            log = InventoryLog(
                product_id=product.id,
                type='out',
                quantity=quantity,
                stock_date=log_date,
                status=InventoryStatus.COMPLETED,
                notes=f'Job site delivery - DR-{random.randint(1000, 9999)}'
            )
            db.session.add(log)
    
    db.session.commit()
    print("Inventory logs seeded")

if __name__ == '__main__':
    with app.app_context():
        print("Seeding construction industry sample data...")
        clear_existing_data()
        seed_categories()
        seed_products()
        seed_customers()
        seed_employee_users()
        seed_sales()
        seed_payroll()
        seed_inventory_logs()
        print("Construction sample data seeding complete!")
