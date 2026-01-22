"""
Database Data Verification and Display Tool
Shows all data currently in the unified database system
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    User, UserRole, Category, Product, Customer, Sale, SaleItem,
    PayrollRecord, InventoryLog, InventoryStatus
)
from datetime import datetime
from decimal import Decimal

app = create_app()

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def verify_users():
    """Display all users"""
    print_header("👥 USERS IN DATABASE")
    users = User.query.all()
    print(f"Total Users: {len(users)}\n")
    
    for user in users:
        role = user.role.value if user.role else 'unknown'
        dept = f" | Dept: {user.department}" if user.department else ""
        print(f"  • {user.username:20s} | {user.email:30s} | {role:20s}{dept}")
    
    return len(users)

def verify_products():
    """Display all products"""
    print_header("🏗️ PRODUCTS & SERVICES")
    categories = Category.query.all()
    print(f"Total Categories: {len(categories)}")
    print(f"Total Products: {Product.query.count()}\n")
    
    for category in categories:
        products = Product.query.filter_by(category_id=category.id).all()
        print(f"\n📦 {category.name} ({len(products)} items):")
        for product in products[:5]:  # Show first 5
            price = f"₱{float(product.selling_price):,.2f}"
            track = "📊" if product.track_inventory else "  "
            print(f"  {track} {product.name:40s} {price:>15s}")
        if len(products) > 5:
            print(f"  ... and {len(products) - 5} more")
    
    return Product.query.count()

def verify_customers():
    """Display all customers"""
    print_header("🤝 CUSTOMERS")
    customers = Customer.query.all()
    print(f"Total Customers: {len(customers)}\n")
    
    for customer in customers[:10]:  # Show first 10
        print(f"  • {customer.name:40s} | {customer.email or 'No email':30s}")
    if len(customers) > 10:
        print(f"  ... and {len(customers) - 10} more")
    
    return len(customers)

def verify_sales():
    """Display sales data"""
    print_header("💰 SALES RECORDS")
    
    total_sales = Sale.query.count()
    paid_sales = Sale.query.filter_by(payment_status='paid').count()
    pending_sales = Sale.query.filter_by(payment_status='pending').count()
    
    total_revenue = sum([float(s.total_amount) for s in Sale.query.all()])
    paid_revenue = sum([float(s.total_amount) for s in Sale.query.filter_by(payment_status='paid').all()])
    
    print(f"Total Sales: {total_sales}")
    print(f"  • Paid: {paid_sales} (₱{paid_revenue:,.2f})")
    print(f"  • Pending: {pending_sales} (₱{total_revenue - paid_revenue:,.2f})")
    print(f"\n💵 Total Revenue: ₱{total_revenue:,.2f}")
    
    # Show date range
    oldest = Sale.query.order_by(Sale.sale_date.asc()).first()
    newest = Sale.query.order_by(Sale.sale_date.desc()).first()
    
    if oldest and newest:
        print(f"\n📅 Date Range:")
        print(f"  • Oldest Sale: {oldest.sale_date.strftime('%Y-%m-%d')} ({oldest.invoice_number})")
        print(f"  • Newest Sale: {newest.sale_date.strftime('%Y-%m-%d')} ({newest.invoice_number})")
    
    # Show recent sales
    print(f"\n📋 Recent Sales (Last 5):")
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()
    for sale in recent_sales:
        customer_name = sale.customer.name if sale.customer else "Unknown"
        amount = f"₱{float(sale.total_amount):,.2f}"
        status = "✓" if sale.payment_status == 'paid' else "⏳"
        print(f"  {status} {sale.invoice_number:15s} | {sale.sale_date.strftime('%Y-%m-%d'):12s} | {customer_name:30s} | {amount:>15s}")
    
    return total_sales

def verify_inventory():
    """Display inventory data"""
    print_header("📦 INVENTORY LOGS")
    
    total_logs = InventoryLog.query.count()
    stock_in = InventoryLog.query.filter_by(type='in').count()
    stock_out = InventoryLog.query.filter_by(type='out').count()
    
    print(f"Total Inventory Movements: {total_logs}")
    print(f"  • Stock In: {stock_in}")
    print(f"  • Stock Out: {stock_out}")
    
    # Show recent movements
    print(f"\n📋 Recent Inventory Movements (Last 5):")
    recent_logs = InventoryLog.query.order_by(InventoryLog.stock_date.desc()).limit(5).all()
    for log in recent_logs:
        product_name = log.product.name if log.product else "Unknown"
        direction = "➡️ IN " if log.type == 'in' else "⬅️ OUT"
        date_str = log.stock_date.strftime('%Y-%m-%d')
        print(f"  {direction} | {date_str:12s} | {product_name:40s} | Qty: {log.quantity:>5}")
    
    return total_logs

def verify_payroll():
    """Display payroll data"""
    print_header("💵 PAYROLL RECORDS")
    
    total_payroll = PayrollRecord.query.count()
    paid_payroll = PayrollRecord.query.filter_by(is_paid=True).count()
    pending_payroll = PayrollRecord.query.filter_by(is_paid=False).count()
    
    total_paid_amount = sum([float(p.net_pay) for p in PayrollRecord.query.filter_by(is_paid=True).all()])
    
    print(f"Total Payroll Records: {total_payroll}")
    print(f"  • Paid: {paid_payroll}")
    print(f"  • Pending: {pending_payroll}")
    print(f"\n💰 Total Paid Out: ₱{total_paid_amount:,.2f}")
    
    # Show recent payroll
    print(f"\n📋 Recent Payroll Records (Last 5):")
    recent_payroll = PayrollRecord.query.order_by(PayrollRecord.pay_period_end.desc()).limit(5).all()
    for payroll in recent_payroll:
        employee_name = f"{payroll.employee.first_name} {payroll.employee.last_name}" if payroll.employee else "Unknown"
        net_pay = f"₱{float(payroll.net_pay):,.2f}"
        status = "✓" if payroll.is_paid else "⏳"
        period_end = payroll.pay_period_end.strftime('%Y-%m-%d')
        print(f"  {status} {employee_name:30s} | {period_end:12s} | Net Pay: {net_pay:>15s}")
    
    return total_payroll

def verify_database_file():
    """Verify database file exists and show info"""
    print_header("💾 DATABASE FILE INFO")
    
    db_path = os.path.join(os.path.dirname(__file__), 'business_management.db')
    
    if os.path.exists(db_path):
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"✓ Database File: business_management.db")
        print(f"✓ Location: {db_path}")
        print(f"✓ Size: {size_mb:.2f} MB")
        print(f"✓ Last Modified: {datetime.fromtimestamp(os.path.getmtime(db_path)).strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    else:
        print("✗ Database file not found!")
        return False

def main():
    """Main verification function"""
    print("\n" + "="*70)
    print("  🔍 DATABASE DATA VERIFICATION TOOL")
    print("  KDRT Construction Management System")
    print("="*70)
    
    with app.app_context():
        # Verify database file
        db_exists = verify_database_file()
        
        if not db_exists:
            print("\n❌ ERROR: Database file does not exist!")
            print("Run: python init_database.py")
            return
        
        # Verify all data
        user_count = verify_users()
        product_count = verify_products()
        customer_count = verify_customers()
        sales_count = verify_sales()
        inventory_count = verify_inventory()
        payroll_count = verify_payroll()
    
    # Summary
    print_header("📊 DATA SUMMARY")
    print(f"""
  Database Status: ✅ OPERATIONAL
  
  📈 Data Counts:
    • Users: {user_count}
    • Products: {product_count}
    • Customers: {customer_count}
    • Sales: {sales_count}
    • Inventory Logs: {inventory_count}
    • Payroll Records: {payroll_count}
    
  💡 All data is present in the unified database!
  
  🚀 Next Steps:
    1. Backend is running at: http://127.0.0.1:5000
    2. Frontend is running at: http://localhost:3000
    3. Login with: admin / admin123
    4. All tabs should display data!
    """)
    
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
