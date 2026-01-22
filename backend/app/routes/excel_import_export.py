"""
Excel Import/Export routes for all modules
Supports uploading Excel files and downloading data as Excel
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import os
from io import BytesIO
from datetime import datetime
from app import db
from app.models import Product, Category, Customer, Sale, SaleItem, User, PayrollRecord
from flask_jwt_extended import jwt_required, get_jwt_identity

excel_bp = Blueprint('excel', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== PRODUCT IMPORT/EXPORT ====================

@excel_bp.route('/products/export', methods=['GET'])
@jwt_required()
def export_products():
    """Export all products to Excel"""
    try:
        products = Product.query.all()
        
        data = []
        for product in products:
            data.append({
                'ID': product.id,
                'Name': product.name,
                'SKU': product.sku,
                'Description': product.description,
                'Category': product.category.name if product.category else '',
                'Item Cost': float(product.item_cost) if product.item_cost else 0,
                'Selling Price': float(product.selling_price) if product.selling_price else 0,
                'Is Service': 'Yes' if product.is_service else 'No',
                'Track Inventory': 'Yes' if product.track_inventory else 'No',
                'Current Stock': product.current_stock,
                'Low Stock Threshold': product.low_stock_threshold,
                'Created At': product.created_at.strftime('%Y-%m-%d %H:%M:%S') if product.created_at else ''
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'products_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@excel_bp.route('/products/import', methods=['POST'])
@jwt_required()
def import_products():
    """Import products from Excel file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload .xlsx or .xls file'}), 400
        
        # Read Excel file
        df = pd.read_excel(file)
        
        imported_count = 0
        updated_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Check if product with SKU already exists
                sku = str(row.get('SKU', '')).strip()
                if not sku:
                    errors.append(f"Row {index + 2}: SKU is required")
                    continue
                
                product = Product.query.filter_by(sku=sku).first()
                
                # Get or create category
                category = None
                category_name = str(row.get('Category', '')).strip()
                if category_name:
                    category = Category.query.filter_by(name=category_name).first()
                    if not category:
                        category = Category(name=category_name)
                        db.session.add(category)
                        db.session.flush()
                
                # Parse boolean values
                is_service = str(row.get('Is Service', 'No')).strip().lower() in ['yes', 'true', '1']
                track_inventory = str(row.get('Track Inventory', 'Yes')).strip().lower() in ['yes', 'true', '1']
                
                if product:
                    # Update existing product
                    product.name = str(row.get('Name', product.name))
                    product.description = str(row.get('Description', product.description or ''))
                    product.category_id = category.id if category else product.category_id
                    product.item_cost = float(row.get('Item Cost', product.item_cost or 0))
                    product.selling_price = float(row.get('Selling Price', product.selling_price or 0))
                    product.is_service = is_service
                    product.track_inventory = track_inventory
                    product.current_stock = int(row.get('Current Stock', product.current_stock or 0))
                    product.low_stock_threshold = int(row.get('Low Stock Threshold', product.low_stock_threshold or 10))
                    updated_count += 1
                else:
                    # Create new product
                    product = Product(
                        name=str(row.get('Name', '')),
                        sku=sku,
                        description=str(row.get('Description', '')),
                        category_id=category.id if category else None,
                        item_cost=float(row.get('Item Cost', 0)),
                        selling_price=float(row.get('Selling Price', 0)),
                        is_service=is_service,
                        track_inventory=track_inventory,
                        current_stock=int(row.get('Current Stock', 0)),
                        low_stock_threshold=int(row.get('Low Stock Threshold', 10))
                    )
                    db.session.add(product)
                    imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': 'Import completed',
            'imported': imported_count,
            'updated': updated_count,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== SALES IMPORT/EXPORT ====================

@excel_bp.route('/sales/export', methods=['GET'])
@jwt_required()
def export_sales():
    """Export all sales to Excel"""
    try:
        sales = Sale.query.all()
        
        data = []
        for sale in sales:
            for item in sale.items:
                data.append({
                    'Sale ID': sale.id,
                    'Invoice Number': sale.invoice_number,
                    'Sale Date': sale.sale_date.strftime('%Y-%m-%d') if sale.sale_date else '',
                    'Customer': sale.customer.name if sale.customer else 'Walk-in',
                    'Product': item.product.name if item.product else '',
                    'SKU': item.product.sku if item.product else '',
                    'Quantity': item.quantity,
                    'Unit Price': float(item.unit_price),
                    'Discount %': float(item.discount_percentage) if item.discount_percentage else 0,
                    'Line Total': float(item.line_total),
                    'Sale Subtotal': float(sale.subtotal),
                    'Sale Tax': float(sale.tax_amount) if sale.tax_amount else 0,
                    'Sale Total': float(sale.total_amount),
                    'Payment Status': sale.payment_status,
                    'Created At': sale.created_at.strftime('%Y-%m-%d %H:%M:%S') if sale.created_at else ''
                })
        
        df = pd.DataFrame(data)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sales')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'sales_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@excel_bp.route('/sales/import', methods=['POST'])
@jwt_required()
def import_sales():
    """Import sales from Excel file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        df = pd.read_excel(file)
        
        imported_count = 0
        errors = []
        current_sale = None
        current_invoice = None
        
        for index, row in df.iterrows():
            try:
                invoice_number = str(row.get('Invoice Number', '')).strip()
                if not invoice_number:
                    continue
                
                # Check if this is a new sale or continuation of current sale
                if current_invoice != invoice_number:
                    # Create new sale
                    sale_date_str = str(row.get('Sale Date', ''))
                    sale_date = pd.to_datetime(sale_date_str).date() if sale_date_str else datetime.now().date()
                    
                    customer_name = str(row.get('Customer', '')).strip()
                    customer = None
                    if customer_name and customer_name.lower() != 'walk-in':
                        customer = Customer.query.filter_by(name=customer_name).first()
                    
                    current_sale = Sale(
                        invoice_number=invoice_number,
                        sale_date=sale_date,
                        customer_id=customer.id if customer else None,
                        payment_status=str(row.get('Payment Status', 'paid')),
                        subtotal=float(row.get('Sale Subtotal', 0)),
                        tax_amount=float(row.get('Sale Tax', 0)),
                        total_amount=float(row.get('Sale Total', 0)),
                        amount_paid=float(row.get('Sale Total', 0))
                    )
                    db.session.add(current_sale)
                    db.session.flush()
                    current_invoice = invoice_number
                    imported_count += 1
                
                # Add sale item
                sku = str(row.get('SKU', '')).strip()
                if not sku:
                    continue
                
                product = Product.query.filter_by(sku=sku).first()
                if not product:
                    errors.append(f"Row {index + 2}: Product with SKU '{sku}' not found")
                    continue
                
                sale_item = SaleItem(
                    sale_id=current_sale.id,
                    product_id=product.id,
                    quantity=int(row.get('Quantity', 1)),
                    unit_price=float(row.get('Unit Price', 0)),
                    discount_percentage=float(row.get('Discount %', 0)),
                    line_total=float(row.get('Line Total', 0))
                )
                db.session.add(sale_item)
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': 'Import completed',
            'imported': imported_count,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== PAYROLL IMPORT/EXPORT ====================

@excel_bp.route('/payroll/export', methods=['GET'])
@jwt_required()
def export_payroll():
    """Export all payroll records to Excel"""
    try:
        records = PayrollRecord.query.all()
        
        data = []
        for record in records:
            data.append({
                'ID': record.id,
                'Employee': f"{record.employee.first_name} {record.employee.last_name}" if record.employee else '',
                'Employee Email': record.employee.email if record.employee else '',
                'Department': record.employee.department if record.employee else '',
                'Period Start': record.pay_period_start.strftime('%Y-%m-%d') if record.pay_period_start else '',
                'Period End': record.pay_period_end.strftime('%Y-%m-%d') if record.pay_period_end else '',
                'Regular Hours': float(record.regular_hours) if record.regular_hours else 0,
                'Overtime Hours': float(record.overtime_hours) if record.overtime_hours else 0,
                'Hourly Rate': float(record.hourly_rate) if record.hourly_rate else 0,
                'Regular Pay': float(record.regular_pay) if record.regular_pay else 0,
                'Overtime Pay': float(record.overtime_pay) if record.overtime_pay else 0,
                'Bonuses': float(record.bonuses) if record.bonuses else 0,
                'Gross Pay': float(record.gross_pay) if record.gross_pay else 0,
                'Tax Deductions': float(record.tax_deductions) if record.tax_deductions else 0,
                'Insurance Deductions': float(record.insurance_deductions) if record.insurance_deductions else 0,
                'Total Deductions': float(record.total_deductions) if record.total_deductions else 0,
                'Net Pay': float(record.net_pay) if record.net_pay else 0,
                'Is Paid': 'Yes' if record.is_paid else 'No',
                'Payment Date': record.payment_date.strftime('%Y-%m-%d') if record.payment_date else ''
            })
        
        df = pd.DataFrame(data)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Payroll')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'payroll_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@excel_bp.route('/payroll/import', methods=['POST'])
@jwt_required()
def import_payroll():
    """Import payroll records from Excel file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        df = pd.read_excel(file)
        
        imported_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                email = str(row.get('Employee Email', '')).strip()
                if not email:
                    errors.append(f"Row {index + 2}: Employee email is required")
                    continue
                
                employee = User.query.filter_by(email=email).first()
                if not employee:
                    errors.append(f"Row {index + 2}: Employee with email '{email}' not found")
                    continue
                
                period_start = pd.to_datetime(row.get('Period Start')).date()
                period_end = pd.to_datetime(row.get('Period End')).date()
                
                # Check if record already exists
                existing = PayrollRecord.query.filter_by(
                    employee_id=employee.id,
                    pay_period_start=period_start
                ).first()
                
                if existing:
                    errors.append(f"Row {index + 2}: Payroll record already exists for this period")
                    continue
                
                is_paid = str(row.get('Is Paid', 'No')).strip().lower() in ['yes', 'true', '1']
                payment_date = None
                if is_paid and row.get('Payment Date'):
                    payment_date = pd.to_datetime(row.get('Payment Date')).date()
                
                record = PayrollRecord(
                    employee_id=employee.id,
                    pay_period_start=period_start,
                    pay_period_end=period_end,
                    regular_hours=float(row.get('Regular Hours', 0)),
                    overtime_hours=float(row.get('Overtime Hours', 0)),
                    hourly_rate=float(row.get('Hourly Rate', 0)),
                    regular_pay=float(row.get('Regular Pay', 0)),
                    overtime_pay=float(row.get('Overtime Pay', 0)),
                    bonuses=float(row.get('Bonuses', 0)),
                    gross_pay=float(row.get('Gross Pay', 0)),
                    tax_deductions=float(row.get('Tax Deductions', 0)),
                    insurance_deductions=float(row.get('Insurance Deductions', 0)),
                    total_deductions=float(row.get('Total Deductions', 0)),
                    net_pay=float(row.get('Net Pay', 0)),
                    is_paid=is_paid,
                    payment_date=payment_date
                )
                db.session.add(record)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': 'Import completed',
            'imported': imported_count,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== FINANCIAL DATA EXPORT ====================

@excel_bp.route('/financial/export', methods=['GET'])
@jwt_required()
def export_financial():
    """Export financial statements to Excel"""
    try:
        from app.routes.financial import get_statements
        
        statements_response = get_statements()
        statements = statements_response[0].json
        
        # Create multiple sheets for different statements
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Income Statement
            if statements.get('income'):
                income_data = {
                    'Item': [
                        'Sales Revenue', 'Service Revenue', 'Total Revenue',
                        'Cost of Goods Sold', 'Gross Profit',
                        'Payroll Expenses', 'Operating Expenses', 'Operating Income',
                        'Other Income', 'Net Income'
                    ],
                    'Amount': [
                        statements['income'].get('sales_revenue', 0),
                        statements['income'].get('service_revenue', 0),
                        statements['income'].get('total_revenue', 0),
                        statements['income'].get('cost_of_goods_sold', 0),
                        statements['income'].get('gross_profit', 0),
                        statements['income'].get('payroll_expenses', 0),
                        statements['income'].get('operating_expenses', 0),
                        statements['income'].get('operating_income', 0),
                        statements['income'].get('other_income', 0),
                        statements['income'].get('net_income', 0)
                    ]
                }
                df_income = pd.DataFrame(income_data)
                df_income.to_excel(writer, index=False, sheet_name='Income Statement')
            
            # Balance Sheet
            if statements.get('balance'):
                balance_data = {
                    'Item': [
                        'Cash', 'Accounts Receivable', 'Inventory', 'Current Assets',
                        'Non-Current Assets', 'Total Assets',
                        'Accounts Payable', 'Accrued Payroll', 'Current Liabilities',
                        'Long-term Liabilities', 'Total Liabilities',
                        'Shareholders Equity'
                    ],
                    'Amount': [
                        statements['balance'].get('cash', 0),
                        statements['balance'].get('accounts_receivable', 0),
                        statements['balance'].get('inventory_value', 0),
                        statements['balance'].get('current_assets', 0),
                        statements['balance'].get('non_current_assets', 0),
                        statements['balance'].get('total_assets', 0),
                        statements['balance'].get('accounts_payable', 0),
                        statements['balance'].get('accrued_payroll', 0),
                        statements['balance'].get('current_liabilities', 0),
                        statements['balance'].get('long_term_liabilities', 0),
                        statements['balance'].get('total_liabilities', 0),
                        statements['balance'].get('shareholders_equity', 0)
                    ]
                }
                df_balance = pd.DataFrame(balance_data)
                df_balance.to_excel(writer, index=False, sheet_name='Balance Sheet')
            
            # Cash Flow
            if statements.get('cash_flow'):
                cashflow_data = {
                    'Item': ['Net Income', 'Cash from Sales', 'Payroll Payments', 'Net Cash Flow'],
                    'Amount': [
                        statements['cash_flow'].get('net_income', 0),
                        statements['cash_flow'].get('cash_from_sales', 0),
                        statements['cash_flow'].get('payroll_payments', 0),
                        statements['cash_flow'].get('net_cash_flow', 0)
                    ]
                }
                df_cashflow = pd.DataFrame(cashflow_data)
                df_cashflow.to_excel(writer, index=False, sheet_name='Cash Flow')
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'financial_statements_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
