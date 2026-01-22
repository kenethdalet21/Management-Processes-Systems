"""
Enhanced Sample Data Generator for Dashboard and All Tabs Testing
Adds comprehensive data across all modules for complete functionality testing
"""
import os
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    User, UserRole, Category, Product, Customer, Sale, SaleItem,
    PayrollRecord, InventoryLog, InventoryStatus
)

app = create_app()

def enhance_sales_data():
    """Add more sales with varied patterns for dashboard charts"""
    print("Enhancing sales data...")
    
    with app.app_context():
        customers = Customer.query.all()
        products = Product.query.all()
        employees = User.query.filter(User.role != UserRole.ADMIN).all()
        
        if not customers or not products:
            print("Please run seed_construction_data.py first")
            return
        
        # Add 100 more sales across the last 90 days for trend visualization
        existing_sales = Sale.query.count()
        print(f"Current sales count: {existing_sales}")
        
        for i in range(100):
            # Vary dates across last 90 days with more recent activity
            days_ago = random.choices(
                range(90),
                weights=[3 if d < 30 else 1 for d in range(90)],  # More recent sales weighted higher
                k=1
            )[0]
            sale_date = datetime.now() - timedelta(days=days_ago)
            
            customer = random.choice(customers)
            salesperson = random.choice(employees) if employees else None
            
            # Vary number of items per sale
            num_items = random.choices([1, 2, 3, 4, 5], weights=[10, 30, 30, 20, 10], k=1)[0]
            selected_products = random.sample(products, min(num_items, len(products)))
            
            subtotal = 0
            sale_items = []
            
            for product in selected_products:
                # Vary quantities based on product type
                if 'Service' in product.name:
                    quantity = 1
                elif 'Cement' in product.name or 'Blocks' in product.name:
                    quantity = random.randint(10, 100)
                elif 'Concrete' in product.name:
                    quantity = random.randint(5, 50)
                else:
                    quantity = random.randint(1, 30)
                
                unit_price = float(product.selling_price)
                discount_pct = random.choice([0, 0, 0, 5, 10])  # Occasional discounts
                line_total = quantity * unit_price * (1 - discount_pct / 100)
                subtotal += line_total
                
                sale_item = SaleItem(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    discount_percentage=discount_pct,
                    line_total=line_total
                )
                sale_items.append(sale_item)
            
            # Vary payment status (mostly paid, some pending)
            payment_status = random.choices(['paid', 'pending'], weights=[85, 15], k=1)[0]
            
            sale = Sale(
                customer_id=customer.id,
                salesperson_id=salesperson.id if salesperson else None,
                invoice_number=f'INV-2026{str(existing_sales + i + 1).zfill(5)}',
                sale_date=sale_date,
                subtotal=subtotal,
                total_amount=subtotal,
                payment_status=payment_status
            )
            sale.items = sale_items
            db.session.add(sale)
        
        db.session.commit()
        print(f"Added 100 more sales. Total: {Sale.query.count()}")

def enhance_inventory_logs():
    """Add more inventory movements for better tracking"""
    print("Enhancing inventory logs...")
    
    with app.app_context():
        products = Product.query.filter_by(track_inventory=True).all()
        
        # Add movements for all trackable products
        for product in products:
            # Add 5-10 stock movements per product
            movements = random.randint(5, 10)
            
            for i in range(movements):
                days_ago = random.randint(1, 60)
                log_date = datetime.now() - timedelta(days=days_ago)
                
                # Alternate between stock in and stock out
                log_type = 'in' if i % 2 == 0 else 'out'
                
                if log_type == 'in':
                    quantity = random.randint(50, 300)
                    notes = f'Supplier delivery - PO-{random.randint(1000, 9999)}'
                else:
                    quantity = random.randint(10, 100)
                    notes = f'Job site delivery - SO-{random.randint(1000, 9999)}'
                
                log = InventoryLog(
                    product_id=product.id,
                    type=log_type,
                    quantity=quantity,
                    stock_date=log_date,
                    status=InventoryStatus.COMPLETED,
                    notes=notes
                )
                db.session.add(log)
        
        db.session.commit()
        print(f"Total inventory logs: {InventoryLog.query.count()}")

def enhance_payroll_data():
    """Add more payroll periods for trend analysis"""
    print("Enhancing payroll data...")
    
    with app.app_context():
        employees = User.query.filter(User.role != UserRole.ADMIN).all()
        
        # Add 4 more pay periods (2 months of bi-weekly payroll)
        for employee in employees:
            if not employee.hourly_rate:
                continue
            
            for period in range(4):
                period_end = datetime.now() - timedelta(days=15 * (period + 2))  # Start from where seed left off
                period_start = period_end - timedelta(days=14)
                
                regular_hours = random.randint(80, 176)
                overtime_hours = random.randint(0, 25)
                bonuses = random.randint(0, 8000) if random.random() > 0.7 else 0  # Occasional bonuses
                
                regular_pay = regular_hours * float(employee.hourly_rate)
                overtime_pay = overtime_hours * float(employee.hourly_rate) * 1.5
                gross_pay = regular_pay + overtime_pay + bonuses
                
                # Variable deductions
                tax_deductions = gross_pay * random.uniform(0.08, 0.12)
                insurance_deductions = random.randint(500, 1500)
                other_deductions = random.randint(100, 800)
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
                    payment_method=random.choice(['Bank Transfer', 'Check', 'Cash']),
                    is_paid=random.random() > 0.1,  # 90% paid
                    notes=f'Pay period {period + 1} for {employee.department}'
                )
                db.session.add(payroll)
        
        db.session.commit()
        print(f"Total payroll records: {PayrollRecord.query.count()}")

def add_more_customers():
    """Add more construction customers for variety"""
    print("Adding more customers...")
    
    with app.app_context():
        new_customers = [
            {'name': 'Golden Gate Builders', 'email': 'golden@builders.ph', 'phone': '0917-345-6789', 'address': 'Makati City, Metro Manila'},
            {'name': 'Phoenix Construction Group', 'email': 'phoenix@construction.ph', 'phone': '0918-456-7890', 'address': 'Quezon City, Metro Manila'},
            {'name': 'Titan Infrastructure', 'email': 'titan@infrastructure.ph', 'phone': '0919-567-8901', 'address': 'Pasig City, Metro Manila'},
            {'name': 'Summit Developers Co.', 'email': 'summit@developers.ph', 'phone': '0920-678-9012', 'address': 'Mandaluyong City, Metro Manila'},
            {'name': 'Apex Building Solutions', 'email': 'apex@building.ph', 'phone': '0921-789-0123', 'address': 'Taguig City, Metro Manila'},
            {'name': 'Horizon Properties Inc.', 'email': 'horizon@properties.ph', 'phone': '0922-890-1234', 'address': 'BGC, Taguig City'},
            {'name': 'Zenith Construction Corp.', 'email': 'zenith@construction.ph', 'phone': '0923-901-2345', 'address': 'Alabang, Muntinlupa'},
            {'name': 'Pioneer Engineering Works', 'email': 'pioneer@engineering.ph', 'phone': '0924-012-3456', 'address': 'Ortigas, Pasig City'},
        ]
        
        for cust_data in new_customers:
            existing = Customer.query.filter_by(email=cust_data['email']).first()
            if not existing:
                customer = Customer(**cust_data)
                db.session.add(customer)
        
        db.session.commit()
        print(f"Total customers: {Customer.query.count()}")

def display_summary():
    """Display summary of all data for testing"""
    print("\n" + "="*60)
    print("COMPREHENSIVE DATA SUMMARY FOR TESTING")
    print("="*60)
    
    with app.app_context():
        print(f"\n📊 DASHBOARD DATA:")
        print(f"   Total Sales: {Sale.query.count()}")
        print(f"   Total Revenue: ₱{sum([float(s.total_amount) for s in Sale.query.all()]):,.2f}")
        print(f"   Paid Sales: {Sale.query.filter_by(payment_status='paid').count()}")
        print(f"   Pending Sales: {Sale.query.filter_by(payment_status='pending').count()}")
        
        print(f"\n🏗️ PRODUCTS & SERVICES:")
        print(f"   Total Categories: {Category.query.count()}")
        print(f"   Total Products: {Product.query.count()}")
        for category in Category.query.all():
            count = Product.query.filter_by(category_id=category.id).count()
            print(f"   - {category.name}: {count} products")
        
        print(f"\n📦 INVENTORY:")
        print(f"   Trackable Products: {Product.query.filter_by(track_inventory=True).count()}")
        print(f"   Total Inventory Logs: {InventoryLog.query.count()}")
        print(f"   Stock In Movements: {InventoryLog.query.filter_by(type='in').count()}")
        print(f"   Stock Out Movements: {InventoryLog.query.filter_by(type='out').count()}")
        
        print(f"\n🤝 CUSTOMERS:")
        print(f"   Total Customers: {Customer.query.count()}")
        
        print(f"\n👥 EMPLOYEES & PAYROLL:")
        print(f"   Total Employees: {User.query.filter(User.role != UserRole.ADMIN).count()}")
        print(f"   Total Payroll Records: {PayrollRecord.query.count()}")
        print(f"   Paid Payrolls: {PayrollRecord.query.filter_by(is_paid=True).count()}")
        print(f"   Pending Payrolls: {PayrollRecord.query.filter_by(is_paid=False).count()}")
        
        # Date range analysis
        oldest_sale = Sale.query.order_by(Sale.sale_date.asc()).first()
        newest_sale = Sale.query.order_by(Sale.sale_date.desc()).first()
        if oldest_sale and newest_sale:
            print(f"\n📅 DATE RANGE:")
            print(f"   Oldest Sale: {oldest_sale.sale_date.strftime('%Y-%m-%d')}")
            print(f"   Newest Sale: {newest_sale.sale_date.strftime('%Y-%m-%d')}")
            print(f"   Date Span: {(newest_sale.sale_date - oldest_sale.sale_date).days} days")
        
        # Monthly sales for last 3 months
        print(f"\n📈 RECENT SALES TREND (Last 3 Months):")
        for month_offset in range(3):
            start_date = datetime.now() - timedelta(days=30 * (month_offset + 1))
            end_date = datetime.now() - timedelta(days=30 * month_offset)
            month_sales = Sale.query.filter(
                Sale.sale_date.between(start_date, end_date)
            ).count()
            month_revenue = sum([
                float(s.total_amount) for s in Sale.query.filter(
                    Sale.sale_date.between(start_date, end_date)
                ).all()
            ])
            print(f"   {start_date.strftime('%b %Y')}: {month_sales} sales, ₱{month_revenue:,.2f}")
        
        print("\n" + "="*60)
        print("✅ ALL TABS READY FOR TESTING!")
        print("="*60)
        print("\nYou can now:")
        print("1. View comprehensive Dashboard with charts and statistics")
        print("2. Test Product Management with 17 construction products")
        print("3. Test Inventory with detailed movement logs")
        print("4. Test Sales Management with 150+ sales records")
        print("5. Test Payroll Management with multiple pay periods")
        print("6. Test Financial Reports with 90 days of data")
        print("\n")

if __name__ == '__main__':
    print("Starting comprehensive data enhancement...")
    print("This will add more data for better testing and visualization\n")
    
    with app.app_context():
        add_more_customers()
        enhance_sales_data()
        enhance_inventory_logs()
        enhance_payroll_data()
        
    display_summary()
    
    print("\n✨ Data enhancement complete!")
    print("🚀 Refresh your browser to see the updated Dashboard!")
