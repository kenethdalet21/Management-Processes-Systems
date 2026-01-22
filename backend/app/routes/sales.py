from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, Sale, SaleItem, Customer, InventoryLog, User, UserRole
from sqlalchemy import func, extract, and_, or_
from datetime import datetime
from decimal import Decimal

bp = Blueprint('sales', __name__)

def check_permission(user_id, required_roles):
    """Check if user has required role"""
    user = User.query.get(user_id)
    return user and user.role in required_roles


@bp.route('/', methods=['GET'])
@jwt_required()
def get_sales():
    """Get all sales with filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        customer_id = request.args.get('customer_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        
        query = Sale.query
        
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        
        if status:
            query = query.filter_by(payment_status=status)
        
        if start_date:
            query = query.filter(Sale.sale_date >= datetime.fromisoformat(start_date))
        
        if end_date:
            query = query.filter(Sale.sale_date <= datetime.fromisoformat(end_date))
        
        query = query.order_by(Sale.sale_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'sales': [sale.to_dict() for sale in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    """Get a specific sale with items"""
    try:
        sale = Sale.query.get(sale_id)
        
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404
        
        sale_dict = sale.to_dict()
        sale_dict['items'] = [item.to_dict() for item in sale.items]
        
        return jsonify(sale_dict), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/', methods=['POST'])
@jwt_required()
def create_sale():
    """Create a new sale"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        if not data.get('items') or len(data['items']) == 0:
            return jsonify({'error': 'At least one item is required'}), 400
        
        # Create or get customer
        customer_id = data.get('customer_id')
        if not customer_id and data.get('customer_name'):
            customer = Customer(
                name=data['customer_name'],
                email=data.get('customer_email'),
                phone=data.get('customer_phone'),
                address=data.get('customer_address')
            )
            db.session.add(customer)
            db.session.flush()
            customer_id = customer.id
        
        # Calculate totals
        subtotal = Decimal('0')
        items_data = []
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({'error': f'Product {item["product_id"]} not found'}), 404
            
            quantity = int(item['quantity'])
            
            # Check stock if tracking inventory
            if product.track_inventory and product.current_stock < quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            
            unit_price = Decimal(str(item.get('unit_price', product.selling_price)))
            discount = Decimal(str(item.get('discount', 0)))
            line_total = (unit_price * quantity) - discount
            
            items_data.append({
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount': discount,
                'line_total': line_total
            })
            
            subtotal += line_total
        
        # Calculate tax and total
        tax_rate = Decimal(str(data.get('tax_rate', 0)))
        tax_amount = subtotal * (tax_rate / 100)
        discount_total = Decimal(str(data.get('discount', 0)))
        total_amount = subtotal + tax_amount - discount_total
        
        # Generate invoice number
        today = datetime.now()
        count = Sale.query.filter(func.date(Sale.sale_date) == today.date()).count()
        invoice_number = f"INV-{today.strftime('%Y%m%d')}-{count + 1:04d}"
        
        # Create sale
        sale = Sale(
            invoice_number=invoice_number,
            customer_id=customer_id,
            salesperson_id=user_id,
            sale_date=datetime.now(),
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            discount=discount_total,
            total_amount=total_amount,
            payment_method=data.get('payment_method', 'cash'),
            payment_status=data.get('payment_status', 'paid'),
            notes=data.get('notes', '')
        )
        
        db.session.add(sale)
        db.session.flush()
        
        # Create sale items and update inventory
        for item_data in items_data:
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item_data['product'].id,
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                discount=item_data['discount'],
                line_total=item_data['line_total']
            )
            db.session.add(sale_item)
            
            # Update inventory
            product = item_data['product']
            if product.track_inventory:
                previous_stock = product.current_stock
                product.current_stock -= item_data['quantity']
                
                log = InventoryLog(
                    product_id=product.id,
                    log_type='out',
                    quantity=item_data['quantity'],
                    previous_stock=previous_stock,
                    new_stock=product.current_stock,
                    unit_cost=float(product.item_cost),
                    reference=invoice_number,
                    notes=f'Sale {invoice_number}',
                    performed_by=user_id
                )
                db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Sale created successfully',
            'sale': sale.to_dict(),
            'invoice_number': invoice_number
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:sale_id>', methods=['PUT'])
@jwt_required()
def update_sale(sale_id):
    """Update a sale (limited updates allowed)"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        sale = Sale.query.get(sale_id)
        
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404
        
        data = request.get_json()
        
        # Only allow updating certain fields
        if 'payment_status' in data:
            sale.payment_status = data['payment_status']
        if 'payment_method' in data:
            sale.payment_method = data['payment_method']
        if 'notes' in data:
            sale.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Sale updated successfully',
            'sale': sale.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:sale_id>', methods=['DELETE'])
@jwt_required()
def delete_sale(sale_id):
    """Delete a sale (void)"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_permission(user_id, [UserRole.ADMIN]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        sale = Sale.query.get(sale_id)
        
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404
        
        # Restore inventory
        for item in sale.items:
            product = Product.query.get(item.product_id)
            if product and product.track_inventory:
                previous_stock = product.current_stock
                product.current_stock += item.quantity
                
                log = InventoryLog(
                    product_id=product.id,
                    log_type='in',
                    quantity=item.quantity,
                    previous_stock=previous_stock,
                    new_stock=product.current_stock,
                    unit_cost=float(product.item_cost),
                    reference=f'VOID-{sale.invoice_number}',
                    notes=f'Voided sale {sale.invoice_number}',
                    performed_by=user_id
                )
                db.session.add(log)
        
        # Delete sale items first
        SaleItem.query.filter_by(sale_id=sale_id).delete()
        db.session.delete(sale)
        db.session.commit()
        
        return jsonify({'message': 'Sale voided successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Customer routes
@bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """Get all customers"""
    try:
        customers = Customer.query.order_by(Customer.name).all()
        return jsonify({
            'customers': [c.to_dict() for c in customers]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        customer = Customer(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer created successfully',
            'customer': customer.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/analysis', methods=['GET'])
@jwt_required()
def get_sales_analysis():
    """Get sales analysis"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        # Monthly totals
        monthly_sales = db.session.query(func.sum(Sale.total_amount)).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).scalar() or 0
        
        monthly_count = Sale.query.filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).count()
        
        # Daily breakdown
        daily_sales = db.session.query(
            func.date(Sale.sale_date),
            func.sum(Sale.total_amount),
            func.count(Sale.id)
        ).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).group_by(func.date(Sale.sale_date)).all()
        
        # Top customers
        top_customers = db.session.query(
            Customer.name,
            func.sum(Sale.total_amount).label('total'),
            func.count(Sale.id).label('orders')
        ).join(Sale).filter(
            extract('year', Sale.sale_date) == year,
            extract('month', Sale.sale_date) == month
        ).group_by(Customer.id, Customer.name).order_by(
            func.sum(Sale.total_amount).desc()
        ).limit(5).all()
        
        return jsonify({
            'period': {'year': year, 'month': month},
            'summary': {
                'total_sales': round(float(monthly_sales), 2),
                'order_count': monthly_count,
                'average_order': round(float(monthly_sales) / monthly_count, 2) if monthly_count > 0 else 0
            },
            'daily_breakdown': [
                {
                    'date': str(item[0]),
                    'sales': round(float(item[1]), 2),
                    'orders': int(item[2])
                } for item in daily_sales
            ],
            'top_customers': [
                {
                    'name': item[0] or 'Walk-in Customer',
                    'total': round(float(item[1]), 2),
                    'orders': int(item[2])
                } for item in top_customers
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
