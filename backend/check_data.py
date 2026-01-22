from app import create_app, db
from app.models import Sale, Product, PayrollRecord, SaleItem
from sqlalchemy import func

app = create_app()

with app.app_context():
    print("\n=== DATABASE STATUS ===")
    print(f"Sales count: {Sale.query.count()}")
    print(f"Products count: {Product.query.count()}")
    print(f"Payroll records: {PayrollRecord.query.count()}")
    
    total_revenue = db.session.query(func.sum(Sale.total_amount)).scalar() or 0
    print(f"Total revenue: ₱{float(total_revenue):,.2f}")
    
    # Get recent sales
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()
    print("\n=== RECENT SALES ===")
    for sale in recent_sales:
        print(f"Invoice: {sale.invoice_number} | Date: {sale.sale_date.date()} | Total: ₱{float(sale.total_amount):,.2f}")
    
    # Get product inventory
    print("\n=== INVENTORY STATUS ===")
    total_products = Product.query.count()
    in_stock = Product.query.filter(Product.current_stock > Product.low_stock_threshold).count()
    low_stock = Product.query.filter(
        Product.current_stock > 0,
        Product.current_stock <= Product.low_stock_threshold
    ).count()
    out_of_stock = Product.query.filter(Product.current_stock == 0, Product.track_inventory == True).count()
    
    print(f"Total Products: {total_products}")
    print(f"In Stock: {in_stock}")
    print(f"Low Stock: {low_stock}")
    print(f"Out of Stock: {out_of_stock}")
    
    # Get payroll summary
    print("\n=== PAYROLL SUMMARY ===")
    total_gross = db.session.query(func.sum(PayrollRecord.gross_pay)).scalar() or 0
    total_net = db.session.query(func.sum(PayrollRecord.net_pay)).scalar() or 0
    pending = PayrollRecord.query.filter_by(is_paid=False).count()
    
    print(f"Total Gross Pay: ₱{float(total_gross):,.2f}")
    print(f"Total Net Pay: ₱{float(total_net):,.2f}")
    print(f"Pending Payments: {pending}")
    
    print("\n=== TOP 5 SELLING PRODUCTS ===")
    top_products = db.session.query(
        Product.name,
        func.sum(SaleItem.quantity).label('qty'),
        func.sum(SaleItem.line_total).label('revenue')
    ).join(SaleItem).join(Sale).group_by(Product.id, Product.name).order_by(
        func.sum(SaleItem.line_total).desc()
    ).limit(5).all()
    
    for i, (name, qty, revenue) in enumerate(top_products, 1):
        print(f"{i}. {name}: {int(qty)} units sold | ₱{float(revenue):,.2f} revenue")
