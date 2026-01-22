"""
Comprehensive seed script for Office Supplies Inventory and all business data.
Creates sample data for Products, Services, Inventory, Sales, Customers, and Payroll.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, date, timedelta
from decimal import Decimal
import random
from app import create_app, db
from app.models import (
    User, UserRole, Category, Product, InventoryLog, InventoryStatus,
    Customer, Sale, SaleItem, PayrollRecord
)
from werkzeug.security import generate_password_hash

def clear_existing_data():
    """Clear existing sample data but keep users"""
    print("Clearing existing data...")
    SaleItem.query.delete()
    Sale.query.delete()
    InventoryLog.query.delete()
    Product.query.delete()
    Category.query.delete()
    Customer.query.delete()
    PayrollRecord.query.delete()
    db.session.commit()
    print("✓ Existing data cleared")

def create_categories():
    """Create product categories including Office Supplies"""
    print("Creating categories...")
    categories = [
        # Office Supplies Categories
        {"name": "Office Supplies", "description": "General office supplies and stationery"},
        {"name": "Paper Products", "description": "Papers, notebooks, and printing materials"},
        {"name": "Writing Instruments", "description": "Pens, pencils, markers, and highlighters"},
        {"name": "Filing & Organization", "description": "Folders, binders, and filing supplies"},
        {"name": "Computer Accessories", "description": "USB drives, mouse pads, and cables"},
        {"name": "Desk Accessories", "description": "Staplers, tape dispensers, and desk organizers"},
        # Construction Materials
        {"name": "Building Materials", "description": "Cement, sand, gravel, and aggregates"},
        {"name": "Hardware", "description": "Nails, screws, bolts, and fasteners"},
        {"name": "Tools", "description": "Power tools and hand tools"},
        {"name": "Safety Equipment", "description": "Hard hats, gloves, and safety gear"},
        # Services
        {"name": "Professional Services", "description": "Consulting and professional services"},
        {"name": "Maintenance Services", "description": "Repair and maintenance services"},
    ]
    
    created_categories = {}
    for cat_data in categories:
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()
        created_categories[cat_data["name"]] = category
    
    db.session.commit()
    print(f"✓ Created {len(categories)} categories")
    return created_categories

def create_products(categories):
    """Create products including Office Supplies inventory"""
    print("Creating products...")
    
    products_data = [
        # Office Supplies
        {"name": "Bond Paper A4 (Ream)", "sku": "OFF-001", "category": "Paper Products", "item_cost": 180, "selling_price": 250, "stock": 150, "threshold": 20},
        {"name": "Bond Paper Legal (Ream)", "sku": "OFF-002", "category": "Paper Products", "item_cost": 200, "selling_price": 280, "stock": 120, "threshold": 20},
        {"name": "Yellow Pad Legal", "sku": "OFF-003", "category": "Paper Products", "item_cost": 25, "selling_price": 45, "stock": 200, "threshold": 30},
        {"name": "Notebook 80 Leaves", "sku": "OFF-004", "category": "Paper Products", "item_cost": 35, "selling_price": 55, "stock": 180, "threshold": 25},
        {"name": "Sticky Notes 3x3 (Pack)", "sku": "OFF-005", "category": "Paper Products", "item_cost": 45, "selling_price": 75, "stock": 100, "threshold": 15},
        {"name": "Index Cards (Pack of 100)", "sku": "OFF-006", "category": "Paper Products", "item_cost": 30, "selling_price": 50, "stock": 80, "threshold": 10},
        
        {"name": "Ballpoint Pen Black (Box)", "sku": "PEN-001", "category": "Writing Instruments", "item_cost": 120, "selling_price": 180, "stock": 50, "threshold": 10},
        {"name": "Ballpoint Pen Blue (Box)", "sku": "PEN-002", "category": "Writing Instruments", "item_cost": 120, "selling_price": 180, "stock": 45, "threshold": 10},
        {"name": "Gel Pen Black (Box)", "sku": "PEN-003", "category": "Writing Instruments", "item_cost": 180, "selling_price": 280, "stock": 40, "threshold": 8},
        {"name": "Pencil #2 (Box of 12)", "sku": "PEN-004", "category": "Writing Instruments", "item_cost": 60, "selling_price": 95, "stock": 60, "threshold": 10},
        {"name": "Highlighter Set (6 colors)", "sku": "PEN-005", "category": "Writing Instruments", "item_cost": 85, "selling_price": 135, "stock": 35, "threshold": 8},
        {"name": "Permanent Marker Black", "sku": "PEN-006", "category": "Writing Instruments", "item_cost": 35, "selling_price": 55, "stock": 70, "threshold": 12},
        {"name": "Whiteboard Marker Set", "sku": "PEN-007", "category": "Writing Instruments", "item_cost": 95, "selling_price": 150, "stock": 30, "threshold": 5},
        
        {"name": "Folder Long Brown (Pack)", "sku": "FIL-001", "category": "Filing & Organization", "item_cost": 85, "selling_price": 130, "stock": 100, "threshold": 15},
        {"name": "Folder Short Brown (Pack)", "sku": "FIL-002", "category": "Filing & Organization", "item_cost": 75, "selling_price": 115, "stock": 90, "threshold": 15},
        {"name": "Clear Folder A4 (Pack)", "sku": "FIL-003", "category": "Filing & Organization", "item_cost": 150, "selling_price": 220, "stock": 60, "threshold": 10},
        {"name": "Ring Binder 2-inch", "sku": "FIL-004", "category": "Filing & Organization", "item_cost": 120, "selling_price": 185, "stock": 40, "threshold": 8},
        {"name": "Expanding Envelope Legal", "sku": "FIL-005", "category": "Filing & Organization", "item_cost": 45, "selling_price": 75, "stock": 75, "threshold": 12},
        {"name": "File Box Organizer", "sku": "FIL-006", "category": "Filing & Organization", "item_cost": 250, "selling_price": 380, "stock": 20, "threshold": 5},
        
        {"name": "USB Flash Drive 32GB", "sku": "COM-001", "category": "Computer Accessories", "item_cost": 280, "selling_price": 420, "stock": 25, "threshold": 5},
        {"name": "USB Flash Drive 64GB", "sku": "COM-002", "category": "Computer Accessories", "item_cost": 420, "selling_price": 620, "stock": 20, "threshold": 5},
        {"name": "Mouse Pad Standard", "sku": "COM-003", "category": "Computer Accessories", "item_cost": 80, "selling_price": 130, "stock": 35, "threshold": 8},
        {"name": "USB Cable Type-C", "sku": "COM-004", "category": "Computer Accessories", "item_cost": 150, "selling_price": 250, "stock": 30, "threshold": 6},
        {"name": "HDMI Cable 1.5m", "sku": "COM-005", "category": "Computer Accessories", "item_cost": 180, "selling_price": 290, "stock": 25, "threshold": 5},
        {"name": "Keyboard Wireless", "sku": "COM-006", "category": "Computer Accessories", "item_cost": 650, "selling_price": 950, "stock": 15, "threshold": 3},
        {"name": "Mouse Wireless", "sku": "COM-007", "category": "Computer Accessories", "item_cost": 450, "selling_price": 680, "stock": 18, "threshold": 4},
        
        {"name": "Stapler Heavy Duty", "sku": "DSK-001", "category": "Desk Accessories", "item_cost": 350, "selling_price": 520, "stock": 20, "threshold": 4},
        {"name": "Stapler Standard", "sku": "DSK-002", "category": "Desk Accessories", "item_cost": 85, "selling_price": 135, "stock": 35, "threshold": 8},
        {"name": "Staple Wire No. 35", "sku": "DSK-003", "category": "Desk Accessories", "item_cost": 45, "selling_price": 70, "stock": 80, "threshold": 15},
        {"name": "Tape Dispenser", "sku": "DSK-004", "category": "Desk Accessories", "item_cost": 75, "selling_price": 120, "stock": 25, "threshold": 5},
        {"name": "Scotch Tape 1-inch", "sku": "DSK-005", "category": "Desk Accessories", "item_cost": 35, "selling_price": 55, "stock": 100, "threshold": 20},
        {"name": "Paper Clip Jumbo (Box)", "sku": "DSK-006", "category": "Desk Accessories", "item_cost": 25, "selling_price": 40, "stock": 120, "threshold": 25},
        {"name": "Binder Clip 1-inch (Box)", "sku": "DSK-007", "category": "Desk Accessories", "item_cost": 35, "selling_price": 55, "stock": 90, "threshold": 18},
        {"name": "Scissors 7-inch", "sku": "DSK-008", "category": "Desk Accessories", "item_cost": 65, "selling_price": 100, "stock": 30, "threshold": 6},
        {"name": "Desk Organizer 4-Tier", "sku": "DSK-009", "category": "Desk Accessories", "item_cost": 280, "selling_price": 420, "stock": 12, "threshold": 3},
        {"name": "Pen Holder Cup", "sku": "DSK-010", "category": "Desk Accessories", "item_cost": 45, "selling_price": 75, "stock": 40, "threshold": 8},
        
        # Construction Materials
        {"name": "Portland Cement 40kg", "sku": "CON-001", "category": "Building Materials", "item_cost": 280, "selling_price": 350, "stock": 500, "threshold": 100},
        {"name": "Fine Sand (cubic meter)", "sku": "CON-002", "category": "Building Materials", "item_cost": 800, "selling_price": 1200, "stock": 50, "threshold": 10},
        {"name": "Gravel 3/4 (cubic meter)", "sku": "CON-003", "category": "Building Materials", "item_cost": 900, "selling_price": 1350, "stock": 45, "threshold": 10},
        {"name": "Hollow Block 4-inch", "sku": "CON-004", "category": "Building Materials", "item_cost": 12, "selling_price": 18, "stock": 2000, "threshold": 300},
        {"name": "Steel Bar 10mm (6m)", "sku": "CON-005", "category": "Building Materials", "item_cost": 180, "selling_price": 260, "stock": 200, "threshold": 40},
        {"name": "GI Wire #16 (kg)", "sku": "CON-006", "category": "Building Materials", "item_cost": 85, "selling_price": 120, "stock": 100, "threshold": 20},
        
        {"name": "Common Nail 3-inch (kg)", "sku": "HDW-001", "category": "Hardware", "item_cost": 65, "selling_price": 95, "stock": 150, "threshold": 25},
        {"name": "Concrete Nail 2-inch (kg)", "sku": "HDW-002", "category": "Hardware", "item_cost": 85, "selling_price": 125, "stock": 100, "threshold": 20},
        {"name": "Wood Screw 2-inch (Box)", "sku": "HDW-003", "category": "Hardware", "item_cost": 120, "selling_price": 180, "stock": 80, "threshold": 15},
        {"name": "Bolt & Nut 1/2x3 (Set)", "sku": "HDW-004", "category": "Hardware", "item_cost": 15, "selling_price": 25, "stock": 200, "threshold": 40},
        
        {"name": "Hammer Claw 16oz", "sku": "TLS-001", "category": "Tools", "item_cost": 350, "selling_price": 520, "stock": 15, "threshold": 3},
        {"name": "Measuring Tape 5m", "sku": "TLS-002", "category": "Tools", "item_cost": 120, "selling_price": 180, "stock": 25, "threshold": 5},
        {"name": "Screwdriver Set 6pc", "sku": "TLS-003", "category": "Tools", "item_cost": 280, "selling_price": 420, "stock": 20, "threshold": 4},
        {"name": "Pliers Combination 8-inch", "sku": "TLS-004", "category": "Tools", "item_cost": 180, "selling_price": 280, "stock": 18, "threshold": 4},
        
        {"name": "Hard Hat White", "sku": "SAF-001", "category": "Safety Equipment", "item_cost": 150, "selling_price": 250, "stock": 30, "threshold": 8},
        {"name": "Safety Gloves (Pair)", "sku": "SAF-002", "category": "Safety Equipment", "item_cost": 85, "selling_price": 130, "stock": 50, "threshold": 12},
        {"name": "Safety Goggles", "sku": "SAF-003", "category": "Safety Equipment", "item_cost": 120, "selling_price": 190, "stock": 25, "threshold": 6},
        {"name": "Dust Mask N95 (Box 20)", "sku": "SAF-004", "category": "Safety Equipment", "item_cost": 350, "selling_price": 520, "stock": 40, "threshold": 10},
    ]
    
    services_data = [
        {"name": "Office Cleaning Service", "sku": "SVC-001", "category": "Maintenance Services", "item_cost": 800, "selling_price": 1500},
        {"name": "Computer Repair Service", "sku": "SVC-002", "category": "Maintenance Services", "item_cost": 500, "selling_price": 1200},
        {"name": "Printer Maintenance", "sku": "SVC-003", "category": "Maintenance Services", "item_cost": 400, "selling_price": 800},
        {"name": "Network Setup Service", "sku": "SVC-004", "category": "Professional Services", "item_cost": 1500, "selling_price": 3500},
        {"name": "IT Consultation (per hour)", "sku": "SVC-005", "category": "Professional Services", "item_cost": 800, "selling_price": 1500},
        {"name": "Document Binding Service", "sku": "SVC-006", "category": "Professional Services", "item_cost": 50, "selling_price": 150},
        {"name": "Lamination Service A4", "sku": "SVC-007", "category": "Professional Services", "item_cost": 15, "selling_price": 35},
        {"name": "Blueprint Printing (sqm)", "sku": "SVC-008", "category": "Professional Services", "item_cost": 80, "selling_price": 180},
    ]
    
    created_products = []
    
    # Create physical products
    for prod_data in products_data:
        category = categories.get(prod_data["category"])
        product = Product(
            name=prod_data["name"],
            sku=prod_data["sku"],
            description=f"{prod_data['name']} - Quality product for office and business use",
            category_id=category.id if category else None,
            item_cost=Decimal(str(prod_data["item_cost"])),
            tax_amount=Decimal(str(prod_data["item_cost"] * 0.12)),  # 12% VAT
            selling_price=Decimal(str(prod_data["selling_price"])),
            is_service=False,
            track_inventory=True,
            current_stock=prod_data["stock"],
            low_stock_threshold=prod_data["threshold"]
        )
        db.session.add(product)
        created_products.append(product)
    
    # Create services
    for svc_data in services_data:
        category = categories.get(svc_data["category"])
        service = Product(
            name=svc_data["name"],
            sku=svc_data["sku"],
            description=f"{svc_data['name']} - Professional service",
            category_id=category.id if category else None,
            item_cost=Decimal(str(svc_data["item_cost"])),
            selling_price=Decimal(str(svc_data["selling_price"])),
            is_service=True,
            track_inventory=False,
            current_stock=0,
            low_stock_threshold=0
        )
        db.session.add(service)
        created_products.append(service)
    
    db.session.commit()
    print(f"✓ Created {len(products_data)} products and {len(services_data)} services")
    return created_products

def create_inventory_logs(products):
    """Create inventory log entries for all products"""
    print("Creating inventory logs...")
    
    physical_products = [p for p in products if not p.is_service and p.track_inventory]
    logs_created = 0
    
    for product in physical_products:
        # Initial stock entry
        initial_log = InventoryLog(
            product_id=product.id,
            stock_date=datetime.now() - timedelta(days=random.randint(30, 60)),
            quantity=product.current_stock + random.randint(20, 50),
            type="stock_in",
            status=InventoryStatus.COMPLETED,
            notes="Initial inventory stock",
            reference_number=f"INIT-{product.sku}"
        )
        db.session.add(initial_log)
        logs_created += 1
        
        # Random stock movements
        for i in range(random.randint(3, 8)):
            days_ago = random.randint(1, 25)
            is_stock_in = random.choice([True, True, False])  # 2:1 ratio stock in vs out
            qty = random.randint(5, 30)
            
            log = InventoryLog(
                product_id=product.id,
                stock_date=datetime.now() - timedelta(days=days_ago),
                quantity=qty,
                type="stock_in" if is_stock_in else "stock_out",
                status=InventoryStatus.COMPLETED,
                notes="Restocking" if is_stock_in else "Sales fulfillment",
                reference_number=f"{'IN' if is_stock_in else 'OUT'}-{product.sku}-{i+1}"
            )
            db.session.add(log)
            logs_created += 1
    
    # Add some low stock products for alerts
    low_stock_products = random.sample(physical_products, min(8, len(physical_products)))
    for product in low_stock_products:
        product.current_stock = random.randint(1, product.low_stock_threshold - 1)
    
    # Add some out-of-stock products
    out_of_stock = random.sample([p for p in physical_products if p not in low_stock_products], min(3, len(physical_products) - 8))
    for product in out_of_stock:
        product.current_stock = 0
    
    db.session.commit()
    print(f"✓ Created {logs_created} inventory log entries")

def create_customers():
    """Create sample customers"""
    print("Creating customers...")
    
    customers_data = [
        {"name": "ABC Construction Corp.", "email": "procurement@abcconstruction.com", "phone": "+63 917 123 4567", "address": "123 Business Park, Makati City", "tax_id": "123-456-789-000"},
        {"name": "Metro Manila Builders", "email": "orders@mmbuilders.ph", "phone": "+63 918 234 5678", "address": "456 Industrial Ave, Pasig City", "tax_id": "234-567-890-000"},
        {"name": "Prime Office Solutions", "email": "purchasing@primeoffice.com", "phone": "+63 919 345 6789", "address": "789 Corporate Center, BGC", "tax_id": "345-678-901-000"},
        {"name": "Tech Innovations Inc.", "email": "supplies@techinnovations.ph", "phone": "+63 920 456 7890", "address": "101 Tech Hub, Quezon City", "tax_id": "456-789-012-000"},
        {"name": "Green Earth Developers", "email": "admin@greenearth.com", "phone": "+63 921 567 8901", "address": "202 Eco Park, Alabang", "tax_id": "567-890-123-000"},
        {"name": "Golden Star Trading", "email": "orders@goldenstar.ph", "phone": "+63 922 678 9012", "address": "303 Trade Center, Manila", "tax_id": "678-901-234-000"},
        {"name": "Sunrise Property Management", "email": "procurement@sunriseprop.com", "phone": "+63 923 789 0123", "address": "404 Sunrise Bldg, Ortigas", "tax_id": "789-012-345-000"},
        {"name": "Pacific Coast Engineering", "email": "supplies@pacificeng.com", "phone": "+63 924 890 1234", "address": "505 Engineering Complex, Cebu", "tax_id": "890-123-456-000"},
        {"name": "Diamond Home Builders", "email": "purchasing@diamondhome.ph", "phone": "+63 925 901 2345", "address": "606 Builder's Lane, Davao", "tax_id": "901-234-567-000"},
        {"name": "First Class Interiors", "email": "orders@firstclassint.com", "phone": "+63 926 012 3456", "address": "707 Design Center, Makati", "tax_id": "012-345-678-000"},
        {"name": "Mountain View Construction", "email": "admin@mtviewcon.ph", "phone": "+63 927 123 4567", "address": "808 Highland Park, Baguio", "tax_id": "123-456-789-001"},
        {"name": "Ocean Breeze Resort Dev", "email": "procurement@oceanbreeze.com", "phone": "+63 928 234 5678", "address": "909 Beach Road, Boracay", "tax_id": "234-567-890-001"},
        {"name": "City Commercial Center", "email": "supplies@citycenter.ph", "phone": "+63 929 345 6789", "address": "1010 City Mall, Cebu", "tax_id": "345-678-901-001"},
        {"name": "National Infrastructure Corp", "email": "orders@natinfra.gov.ph", "phone": "+63 930 456 7890", "address": "1111 Government Complex, Manila", "tax_id": "456-789-012-001"},
        {"name": "Horizon Development Group", "email": "purchasing@horizondev.com", "phone": "+63 931 567 8901", "address": "1212 Horizon Tower, BGC", "tax_id": "567-890-123-001"},
        {"name": "Royal Office Supplies Co.", "email": "orders@royaloffice.ph", "phone": "+63 932 678 9012", "address": "1313 Royal Building, Makati", "tax_id": "678-901-234-001"},
        {"name": "United Paper Products", "email": "sales@unitedpaper.com", "phone": "+63 933 789 0123", "address": "1414 Paper Mill Road, Laguna", "tax_id": "789-012-345-001"},
        {"name": "Smart Solutions Enterprise", "email": "procurement@smartsolutions.ph", "phone": "+63 934 890 1234", "address": "1515 Smart Building, Pasay", "tax_id": "890-123-456-001"},
        {"name": "Elite Business Services", "email": "orders@elitebiz.com", "phone": "+63 935 901 2345", "address": "1616 Elite Tower, Quezon City", "tax_id": "901-234-567-001"},
        {"name": "Premium Stationery Depot", "email": "sales@premiumstat.ph", "phone": "+63 936 012 3456", "address": "1717 Depot Street, Manila", "tax_id": "012-345-678-001"},
    ]
    
    created_customers = []
    for cust_data in customers_data:
        customer = Customer(**cust_data)
        db.session.add(customer)
        created_customers.append(customer)
    
    db.session.commit()
    print(f"✓ Created {len(customers_data)} customers")
    return created_customers

def create_employees():
    """Create or update employee users for payroll"""
    print("Creating employees...")
    
    employees_data = [
        {"username": "jsmith", "email": "jsmith@company.com", "first_name": "John", "last_name": "Smith", "department": "Operations", "position": "Operations Manager", "hourly_rate": 250, "monthly_salary": 45000},
        {"username": "mgarcia", "email": "mgarcia@company.com", "first_name": "Maria", "last_name": "Garcia", "department": "Sales", "position": "Sales Representative", "hourly_rate": 150, "monthly_salary": 28000},
        {"username": "rcruz", "email": "rcruz@company.com", "first_name": "Roberto", "last_name": "Cruz", "department": "Warehouse", "position": "Warehouse Supervisor", "hourly_rate": 180, "monthly_salary": 32000},
        {"username": "alim", "email": "alim@company.com", "first_name": "Anna", "last_name": "Lim", "department": "Finance", "position": "Accountant", "hourly_rate": 200, "monthly_salary": 38000},
        {"username": "pjose", "email": "pjose@company.com", "first_name": "Pedro", "last_name": "Jose", "department": "IT", "position": "IT Support", "hourly_rate": 175, "monthly_salary": 32000},
        {"username": "ldela", "email": "ldela@company.com", "first_name": "Liza", "last_name": "Dela Cruz", "department": "HR", "position": "HR Coordinator", "hourly_rate": 160, "monthly_salary": 30000},
        {"username": "mreyes", "email": "mreyes@company.com", "first_name": "Miguel", "last_name": "Reyes", "department": "Warehouse", "position": "Stock Clerk", "hourly_rate": 100, "monthly_salary": 18000},
        {"username": "csantos", "email": "csantos@company.com", "first_name": "Carmen", "last_name": "Santos", "department": "Sales", "position": "Sales Associate", "hourly_rate": 120, "monthly_salary": 22000},
        {"username": "jvillanueva", "email": "jvillanueva@company.com", "first_name": "Jose", "last_name": "Villanueva", "department": "Delivery", "position": "Delivery Driver", "hourly_rate": 110, "monthly_salary": 20000},
        {"username": "rfernandez", "email": "rfernandez@company.com", "first_name": "Rosa", "last_name": "Fernandez", "department": "Admin", "position": "Administrative Assistant", "hourly_rate": 130, "monthly_salary": 24000},
        {"username": "emendoza", "email": "emendoza@company.com", "first_name": "Eduardo", "last_name": "Mendoza", "department": "Warehouse", "position": "Inventory Specialist", "hourly_rate": 140, "monthly_salary": 26000},
        {"username": "gaquino", "email": "gaquino@company.com", "first_name": "Gloria", "last_name": "Aquino", "department": "Purchasing", "position": "Purchasing Officer", "hourly_rate": 170, "monthly_salary": 31000},
    ]
    
    created_employees = []
    for emp_data in employees_data:
        # Check if user exists
        existing = User.query.filter_by(username=emp_data["username"]).first()
        if existing:
            # Update existing user
            existing.first_name = emp_data["first_name"]
            existing.last_name = emp_data["last_name"]
            existing.department = emp_data["department"]
            existing.position = emp_data["position"]
            existing.hourly_rate = Decimal(str(emp_data["hourly_rate"]))
            existing.monthly_salary = Decimal(str(emp_data["monthly_salary"]))
            created_employees.append(existing)
        else:
            # Create new user
            user = User(
                username=emp_data["username"],
                email=emp_data["email"],
                password_hash=generate_password_hash("password123"),
                first_name=emp_data["first_name"],
                last_name=emp_data["last_name"],
                role=UserRole.EMPLOYEE,
                is_active=True,
                department=emp_data["department"],
                position=emp_data["position"],
                hourly_rate=Decimal(str(emp_data["hourly_rate"])),
                monthly_salary=Decimal(str(emp_data["monthly_salary"]))
            )
            db.session.add(user)
            created_employees.append(user)
    
    db.session.commit()
    print(f"✓ Created/Updated {len(employees_data)} employees")
    return created_employees

def create_sales(products, customers, employees):
    """Create sample sales transactions"""
    print("Creating sales...")
    
    physical_products = [p for p in products if not p.is_service]
    services = [p for p in products if p.is_service]
    
    sales_created = 0
    
    # Create sales for the past 90 days
    for day_offset in range(90):
        sale_date = datetime.now() - timedelta(days=day_offset)
        num_sales = random.randint(2, 6)  # 2-6 sales per day
        
        for sale_num in range(num_sales):
            customer = random.choice(customers)
            salesperson = random.choice(employees) if employees else None
            
            # Generate invoice number
            invoice_num = f"INV-{sale_date.strftime('%Y%m%d')}-{sale_num + 1:03d}"
            
            # Create sale items
            num_items = random.randint(1, 5)
            items_to_add = random.sample(physical_products, min(num_items, len(physical_products)))
            
            # Add occasional service
            if random.random() > 0.7 and services:
                items_to_add.append(random.choice(services))
            
            subtotal = Decimal("0")
            sale_items = []
            
            for product in items_to_add:
                quantity = random.randint(1, 10)
                unit_price = product.selling_price
                line_discount = Decimal(str(random.choice([0, 0, 0, 5, 10])))  # Occasional discount
                line_total = (unit_price * quantity) * (1 - line_discount / 100)
                subtotal += line_total
                
                sale_items.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": line_discount,
                    "line_total": line_total
                })
            
            # Calculate totals
            discount_pct = Decimal(str(random.choice([0, 0, 0, 5, 10, 15])))
            discount_amt = subtotal * discount_pct / 100
            tax_rate = Decimal("12")
            taxable = subtotal - discount_amt
            tax_amt = taxable * tax_rate / 100
            total = taxable + tax_amt
            
            # Payment status
            payment_status = random.choices(["paid", "paid", "paid", "pending", "partial"], weights=[60, 20, 10, 5, 5])[0]
            amount_paid = total if payment_status == "paid" else (total * Decimal(str(random.uniform(0.3, 0.8))) if payment_status == "partial" else Decimal("0"))
            
            # Create sale
            sale = Sale(
                invoice_number=invoice_num,
                sale_date=sale_date,
                customer_id=customer.id,
                salesperson_id=salesperson.id if salesperson else None,
                subtotal=subtotal,
                discount_percentage=discount_pct,
                discount_amount=discount_amt,
                tax_rate=tax_rate,
                tax_amount=tax_amt,
                total_amount=total,
                payment_status=payment_status,
                amount_paid=amount_paid,
                notes=f"Sale to {customer.name}"
            )
            db.session.add(sale)
            db.session.flush()
            
            # Add sale items
            for item in sale_items:
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=item["product"].id,
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    discount_percentage=item["discount"],
                    line_total=item["line_total"]
                )
                db.session.add(sale_item)
            
            sales_created += 1
    
    db.session.commit()
    print(f"✓ Created {sales_created} sales transactions")

def create_payroll_records(employees):
    """Create payroll records for employees"""
    print("Creating payroll records...")
    
    if not employees:
        print("✗ No employees found for payroll")
        return
    
    records_created = 0
    
    # Create payroll for past 6 months (bi-monthly)
    current_date = date.today()
    
    for month_offset in range(6):
        month_date = current_date - timedelta(days=month_offset * 30)
        year = month_date.year
        month = month_date.month
        
        # First half of month (1-15)
        period1_start = date(year, month, 1)
        period1_end = date(year, month, 15)
        
        # Second half of month (16-end)
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        period2_start = date(year, month, 16)
        period2_end = next_month - timedelta(days=1)
        
        for employee in employees:
            for period_start, period_end in [(period1_start, period1_end), (period2_start, period2_end)]:
                # Skip future periods
                if period_end > current_date:
                    continue
                
                hourly_rate = float(employee.hourly_rate) if employee.hourly_rate else 100
                regular_hours = Decimal(str(random.uniform(75, 88)))  # ~9-11 hours per day
                overtime_hours = Decimal(str(random.uniform(0, 15)))
                overtime_rate = Decimal(str(hourly_rate * 1.25))
                
                regular_pay = regular_hours * Decimal(str(hourly_rate))
                overtime_pay = overtime_hours * overtime_rate
                bonus = Decimal(str(random.choice([0, 0, 0, 500, 1000, 2000])))
                gross_pay = regular_pay + overtime_pay + bonus
                
                # Deductions
                tax_deductions = gross_pay * Decimal("0.10")  # 10% tax
                insurance = Decimal("500")
                other_deductions = Decimal(str(random.choice([0, 0, 200, 300])))
                total_deductions = tax_deductions + insurance + other_deductions
                net_pay = gross_pay - total_deductions
                
                is_paid = month_offset > 0 or period_end < current_date - timedelta(days=5)
                
                record = PayrollRecord(
                    employee_id=employee.id,
                    pay_period_start=period_start,
                    pay_period_end=period_end,
                    regular_hours=regular_hours,
                    overtime_hours=overtime_hours,
                    hourly_rate=Decimal(str(hourly_rate)),
                    overtime_rate=overtime_rate,
                    regular_pay=regular_pay,
                    overtime_pay=overtime_pay,
                    bonuses=bonus,
                    gross_pay=gross_pay,
                    tax_deductions=tax_deductions,
                    insurance_deductions=insurance,
                    other_deductions=other_deductions,
                    total_deductions=total_deductions,
                    net_pay=net_pay,
                    payment_date=period_end + timedelta(days=5) if is_paid else None,
                    payment_method="Bank Transfer" if is_paid else None,
                    is_paid=is_paid,
                    notes=f"Payroll for {period_start} to {period_end}"
                )
                db.session.add(record)
                records_created += 1
    
    db.session.commit()
    print(f"✓ Created {records_created} payroll records")

def add_reference_number_column():
    """Add reference_number column to inventory_logs if it doesn't exist"""
    from sqlalchemy import inspect, text
    
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('inventory_logs')]
    
    if 'reference_number' not in columns:
        print("Adding reference_number column to inventory_logs...")
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE inventory_logs ADD COLUMN reference_number VARCHAR(50)'))
            conn.commit()
        print("✓ Added reference_number column")
    
    if 'balance_after' not in columns:
        print("Adding balance_after column to inventory_logs...")
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE inventory_logs ADD COLUMN balance_after INTEGER DEFAULT 0'))
            conn.commit()
        print("✓ Added balance_after column")

def main():
    """Main function to seed all data"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("   Office Supplies & Business Data Seeding Script")
        print("=" * 60 + "\n")
        
        # Add columns if missing
        add_reference_number_column()
        
        # Clear and recreate data
        clear_existing_data()
        
        # Create all data
        categories = create_categories()
        products = create_products(categories)
        create_inventory_logs(products)
        customers = create_customers()
        employees = create_employees()
        create_sales(products, customers, employees)
        create_payroll_records(employees)
        
        print("\n" + "=" * 60)
        print("   ✓ All sample data created successfully!")
        print("=" * 60)
        
        # Summary
        print(f"\nSummary:")
        print(f"  - Categories: {Category.query.count()}")
        print(f"  - Products: {Product.query.filter_by(is_service=False).count()}")
        print(f"  - Services: {Product.query.filter_by(is_service=True).count()}")
        print(f"  - Inventory Logs: {InventoryLog.query.count()}")
        print(f"  - Customers: {Customer.query.count()}")
        print(f"  - Sales: {Sale.query.count()}")
        print(f"  - Payroll Records: {PayrollRecord.query.count()}")
        print("")

if __name__ == "__main__":
    main()
