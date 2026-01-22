from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, Category, User, UserRole
from sqlalchemy import or_

bp = Blueprint('products', __name__)

def check_permission(user_id, required_roles):
    """Check if user has required role"""
    user = User.query.get(user_id)
    return user and user.role in required_roles

@bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        is_active = request.args.get('is_active', type=bool)
        
        query = Product.query
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.sku.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'products': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Get a specific product"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """Create a new product"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'sku', 'item_cost', 'selling_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if SKU already exists
        if Product.query.filter_by(sku=data['sku']).first():
            return jsonify({'error': 'SKU already exists'}), 400
        
        product = Product(
            name=data['name'],
            sku=data['sku'],
            description=data.get('description'),
            category_id=data.get('category_id'),
            item_cost=data['item_cost'],
            tax_amount=data.get('tax_amount', 0),
            other_costs=data.get('other_costs', 0),
            selling_price=data['selling_price'],
            is_service=data.get('is_service', False),
            track_inventory=data.get('track_inventory', True),
            current_stock=data.get('current_stock', 0),
            low_stock_threshold=data.get('low_stock_threshold', 10)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update a product"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'category_id' in data:
            product.category_id = data['category_id']
        if 'item_cost' in data:
            product.item_cost = data['item_cost']
        if 'tax_amount' in data:
            product.tax_amount = data['tax_amount']
        if 'other_costs' in data:
            product.other_costs = data['other_costs']
        if 'selling_price' in data:
            product.selling_price = data['selling_price']
        if 'low_stock_threshold' in data:
            product.low_stock_threshold = data['low_stock_threshold']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete a product"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Category routes
@bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create a new category"""
    try:
        user_id = get_jwt_identity()
        
        if not check_permission(user_id, [UserRole.ADMIN, UserRole.OPERATIONS_MANAGER]):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        category = Category(
            name=data['name'],
            description=data.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
