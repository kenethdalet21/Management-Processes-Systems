"""
Unified Database Initializer and File Storage Manager
Ensures database exists, is properly initialized, and manages file uploads
"""
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    User, UserRole, Category, Product, Customer, Sale, SaleItem,
    PayrollRecord, InventoryLog, InventoryStatus
)
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / 'uploads'
EXCEL_DIR = UPLOAD_DIR / 'excel'
EXPORT_DIR = UPLOAD_DIR / 'exports'
DATABASE_PATH = BASE_DIR / 'business_management.db'

def ensure_directories():
    """Ensure all required directories exist"""
    print("Ensuring directory structure...")
    directories = [UPLOAD_DIR, EXCEL_DIR, EXPORT_DIR]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory.name}/ created")
    
    print(f"  ✓ Database path: {DATABASE_PATH}")
    return True

def initialize_database():
    """Initialize database with all tables"""
    print("\nInitializing database...")
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("  ✓ All database tables created")
        
        # Check if default admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("  ⚠ No admin user found. Creating default users...")
            create_default_users()
        else:
            print("  ✓ Admin user exists")
        
        return app

def create_default_users():
    """Create default admin and test users"""
    default_users = [
        {
            'username': 'admin',
            'email': 'admin@kdrt.com',
            'password': 'admin123',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': UserRole.ADMIN
        },
        {
            'username': 'finance_mgr',
            'email': 'finance@kdrt.com',
            'password': 'password123',
            'first_name': 'Finance',
            'last_name': 'Manager',
            'role': UserRole.FINANCE_MANAGER,
            'department': 'Finance'
        },
        {
            'username': 'ops_mgr',
            'email': 'operations@kdrt.com',
            'password': 'password123',
            'first_name': 'Operations',
            'last_name': 'Manager',
            'role': UserRole.OPERATIONS_MANAGER,
            'department': 'Operations'
        }
    ]
    
    for user_data in default_users:
        password = user_data.pop('password')
        user = User(**user_data)
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.add(user)
    
    db.session.commit()
    print("  ✓ Default users created")

def check_data_status():
    """Check current data in database"""
    print("\n" + "="*60)
    print("DATABASE STATUS")
    print("="*60)
    
    counts = {
        'Users': User.query.count(),
        'Categories': Category.query.count(),
        'Products': Product.query.count(),
        'Customers': Customer.query.count(),
        'Sales': Sale.query.count(),
        'Sale Items': SaleItem.query.count(),
        'Payroll Records': PayrollRecord.query.count(),
        'Inventory Logs': InventoryLog.query.count()
    }
    
    for table, count in counts.items():
        status = "✓" if count > 0 else "✗"
        print(f"  {status} {table}: {count}")
    
    # Calculate totals
    if counts['Sales'] > 0:
        total_revenue = sum([float(s.total_amount) for s in Sale.query.all()])
        print(f"\n  💰 Total Revenue: ₱{total_revenue:,.2f}")
    
    print("="*60)
    
    return counts

def backup_database():
    """Create a backup of the current database"""
    if DATABASE_PATH.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = BASE_DIR / f'business_management_backup_{timestamp}.db'
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"  ✓ Database backed up to: {backup_path.name}")
        return backup_path
    return None

def get_database_info():
    """Get detailed database information"""
    info = {
        'exists': DATABASE_PATH.exists(),
        'size': DATABASE_PATH.stat().st_size if DATABASE_PATH.exists() else 0,
        'path': str(DATABASE_PATH),
        'upload_dir': str(UPLOAD_DIR),
        'excel_dir': str(EXCEL_DIR),
        'export_dir': str(EXPORT_DIR)
    }
    return info

def main():
    """Main initialization function"""
    print("="*60)
    print("KDRT UNIFIED DATABASE SYSTEM")
    print("="*60)
    
    # Step 1: Ensure directories
    ensure_directories()
    
    # Step 2: Backup existing database
    if DATABASE_PATH.exists():
        print(f"\n📁 Database exists: {DATABASE_PATH.name}")
        backup_database()
    else:
        print(f"\n📁 Creating new database: {DATABASE_PATH.name}")
    
    # Step 3: Initialize database
    app = initialize_database()
    
    # Step 4: Check data status
    with app.app_context():
        counts = check_data_status()
    
    # Step 5: Display info
    info = get_database_info()
    print(f"\n📂 File Storage:")
    print(f"  • Excel Uploads: {info['excel_dir']}")
    print(f"  • Excel Exports: {info['export_dir']}")
    print(f"  • Database Size: {info['size'] / 1024 / 1024:.2f} MB")
    
    # Step 6: Recommendations
    print(f"\n💡 Recommendations:")
    
    if counts['Sales'] == 0:
        print("  ⚠ No sample data found!")
        print("  → Run: python seed_construction_data.py")
        print("  → Then: python enhance_sample_data.py")
    else:
        print("  ✓ Database is ready with sample data!")
        print("  ✓ All systems operational!")
    
    print("\n" + "="*60)
    print("✅ UNIFIED DATABASE SYSTEM INITIALIZED")
    print("="*60)
    print(f"\n🚀 Start backend: python run.py")
    print(f"🌐 Start frontend: npm start (in frontend directory)")
    print(f"🔗 Access at: http://localhost:3000\n")

if __name__ == '__main__':
    main()
