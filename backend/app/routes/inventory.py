from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, InventoryLog, User, UserRole, InventoryStatus
from sqlalchemy import func, extract, and_, or_
from datetime import datetime, timedelta

bp = Blueprint('inventory', __name__)

def check_permission(user_id, required_roles):
    """Check if user has required role"""
    user = User.query.get(user_id)
    return user and user.role in required_roles


@bp.route('/logs', methods=['GET'])
@jwt_required()
def get_inventory_logs():
    """Get all inventory logs with filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        product_id = request.args.get('product_id', type=int)
        log_type = request.args.get('type')  # 'in' or 'out'
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InventoryLog.query
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        if log_type:
            query = query.filter_by(type=log_type)
        
        if start_date:
            query = query.filter(InventoryLog.created_at >= datetime.fromisoformat(start_date))
        
        if end_date:
            query = query.filter(InventoryLog.created_at <= datetime.fromisoformat(end_date))
        
        query = query.order_by(InventoryLog.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'logs': [log.to_dict() for log in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/stock-in', methods=['POST'])
@jwt_required()
def stock_in():
    """Record stock in"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        if not data.get('product_id') or not data.get('quantity'):
            return jsonify({'error': 'product_id and quantity are required'}), 400
        
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
        
        product.current_stock += quantity
        
        log = InventoryLog(
            product_id=product.id,
            type='in',
            quantity=quantity,
            stock_date=datetime.now(),
            status=InventoryStatus.COMPLETED,
            notes=data.get('notes', '')
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Stock in recorded successfully',
            'log': log.to_dict(),
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/stock-out', methods=['POST'])
@jwt_required()
def stock_out():
    """Record stock out"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        if not data.get('product_id') or not data.get('quantity'):
            return jsonify({'error': 'product_id and quantity are required'}), 400
        
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
        
        if product.current_stock < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        product.current_stock -= quantity
        
        log = InventoryLog(
            product_id=product.id,
            type='out',
            quantity=quantity,
            stock_date=datetime.now(),
            status=InventoryStatus.COMPLETED,
            notes=data.get('notes', '')
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Stock out recorded successfully',
            'log': log.to_dict(),
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    """Get products with low or no stock"""
    try:
        low_stock = Product.query.filter(
            and_(
                Product.current_stock > 0,
                Product.current_stock <= Product.low_stock_threshold,
                Product.track_inventory == True
            )
        ).all()
        
        out_of_stock = Product.query.filter(
            and_(
                Product.current_stock == 0,
                Product.track_inventory == True
            )
        ).all()
        
        return jsonify({
            'low_stock': [p.to_dict() for p in low_stock],
            'out_of_stock': [p.to_dict() for p in out_of_stock],
            'low_stock_count': len(low_stock),
            'out_of_stock_count': len(out_of_stock)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/analysis', methods=['GET'])
@jwt_required()
def get_inventory_analysis():
    """Get inventory analysis and valuation"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        # Total inventory value
        products = Product.query.filter_by(track_inventory=True).all()
        
        total_value = sum(float(p.item_cost) * p.current_stock for p in products)
        total_retail_value = sum(float(p.selling_price) * p.current_stock for p in products)
        total_items = sum(p.current_stock for p in products)
        
        # Inventory turnover
        stock_in_month = db.session.query(func.sum(InventoryLog.quantity)).filter(
            InventoryLog.type == 'in',
            extract('year', InventoryLog.created_at) == year,
            extract('month', InventoryLog.created_at) == month
        ).scalar() or 0
        
        stock_out_month = db.session.query(func.sum(InventoryLog.quantity)).filter(
            InventoryLog.type == 'out',
            extract('year', InventoryLog.created_at) == year,
            extract('month', InventoryLog.created_at) == month
        ).scalar() or 0
        
        # Stock movement by category
        movements = db.session.query(
            InventoryLog.type,
            func.sum(InventoryLog.quantity),
            func.count(InventoryLog.id)
        ).filter(
            extract('year', InventoryLog.created_at) == year,
            extract('month', InventoryLog.created_at) == month
        ).group_by(InventoryLog.type).all()
        
        movement_summary = {
            item[0]: {
                'quantity': int(item[1]),
                'transactions': int(item[2])
            } for item in movements
        }
        
        # Top moving products
        top_moving = db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            func.sum(InventoryLog.quantity).label('total_movement')
        ).join(InventoryLog).filter(
            InventoryLog.type == 'out',
            extract('year', InventoryLog.created_at) == year,
            extract('month', InventoryLog.created_at) == month
        ).group_by(Product.id, Product.name, Product.sku).order_by(
            func.sum(InventoryLog.quantity).desc()
        ).limit(10).all()
        
        # Slow moving products (no movement in last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        active_product_ids = db.session.query(InventoryLog.product_id).filter(
            InventoryLog.created_at >= thirty_days_ago
        ).distinct().all()
        active_ids = [p[0] for p in active_product_ids]
        
        slow_moving = Product.query.filter(
            ~Product.id.in_(active_ids) if active_ids else True,
            Product.track_inventory == True,
            Product.current_stock > 0
        ).limit(10).all()
        
        return jsonify({
            'period': {'year': year, 'month': month},
            'valuation': {
                'total_cost_value': round(total_value, 2),
                'total_retail_value': round(total_retail_value, 2),
                'potential_profit': round(total_retail_value - total_value, 2),
                'total_items': total_items,
                'unique_products': len(products)
            },
            'movements': {
                'stock_in': int(stock_in_month),
                'stock_out': int(stock_out_month),
                'net_change': int(stock_in_month) - int(stock_out_month),
                'summary': movement_summary
            },
            'top_moving': [
                {
                    'id': item[0],
                    'name': item[1],
                    'sku': item[2],
                    'movement': int(item[3])
                } for item in top_moving
            ],
            'slow_moving': [p.to_dict() for p in slow_moving]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/products', methods=['GET'])
@jwt_required()
def get_inventory_products():
    """Get all products with inventory info"""
    try:
        products = Product.query.filter_by(track_inventory=True).order_by(Product.name).all()
        
        return jsonify({
            'products': [p.to_dict() for p in products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/logs/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_inventory_log(log_id):
    """Delete an inventory log"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        log = InventoryLog.query.get(log_id)
        if not log:
            return jsonify({'error': 'Inventory log not found'}), 404
        
        # Adjust product stock if needed (reverse the log entry)
        product = Product.query.get(log.product_id)
        if product and product.track_inventory:
            if log.type == 'in' or log.type == 'stock_in':
                product.current_stock -= log.quantity
            elif log.type == 'out' or log.type == 'stock_out':
                product.current_stock += log.quantity
        
        db.session.delete(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Inventory log deleted successfully',
            'product_updated': product.to_dict() if product else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
