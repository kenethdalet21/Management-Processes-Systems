from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, UserRole, TabPermission

bp = Blueprint('settings', __name__)

def check_admin(user_id):
    """Check if user is admin"""
    user = User.query.get(user_id)
    return user and user.role == UserRole.ADMIN

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users for management"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        users = User.query.filter(User.role != UserRole.ADMIN).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tab-permissions', methods=['GET'])
@jwt_required()
def get_tab_permissions():
    """Get all tab permissions"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        # Admin can see all permissions
        if user.role == UserRole.ADMIN:
            permissions = TabPermission.query.all()
        else:
            # Non-admin can only see their own permissions
            permissions = TabPermission.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'permissions': [perm.to_dict() for perm in permissions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tab-permissions/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_tab_permissions(user_id):
    """Get tab permissions for a specific user"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Admin can see any user's permissions, others only their own
        if current_user.role != UserRole.ADMIN and current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        permissions = TabPermission.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'permissions': [perm.to_dict() for perm in permissions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tab-permissions', methods=['POST'])
@jwt_required()
def create_or_update_tab_permission():
    """Create or update a tab permission (Admin only)"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if not data.get('user_id') or not data.get('tab_name'):
            return jsonify({'error': 'user_id and tab_name are required'}), 400
        
        # Check if permission already exists
        existing = TabPermission.query.filter_by(
            user_id=data['user_id'],
            tab_name=data['tab_name']
        ).first()
        
        if existing:
            # Update existing permission
            existing.is_locked = data.get('is_locked', existing.is_locked)
            db.session.commit()
            return jsonify({
                'message': 'Permission updated',
                'permission': existing.to_dict()
            }), 200
        else:
            # Create new permission
            permission = TabPermission(
                user_id=data['user_id'],
                tab_name=data['tab_name'],
                is_locked=data.get('is_locked', False)
            )
            db.session.add(permission)
            db.session.commit()
            
            return jsonify({
                'message': 'Permission created',
                'permission': permission.to_dict()
            }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/tab-permissions/bulk', methods=['POST'])
@jwt_required()
def bulk_update_tab_permissions():
    """Bulk update tab permissions for a user (Admin only)"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        target_user_id = data.get('user_id')
        permissions = data.get('permissions', {})  # {tab_name: is_locked}
        
        if not target_user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Delete existing permissions for this user
        TabPermission.query.filter_by(user_id=target_user_id).delete()
        
        # Create new permissions
        for tab_name, is_locked in permissions.items():
            permission = TabPermission(
                user_id=target_user_id,
                tab_name=tab_name,
                is_locked=is_locked
            )
            db.session.add(permission)
        
        db.session.commit()
        
        # Return updated permissions
        updated_permissions = TabPermission.query.filter_by(user_id=target_user_id).all()
        
        return jsonify({
            'message': 'Permissions updated successfully',
            'permissions': [perm.to_dict() for perm in updated_permissions]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/tab-permissions/<int:permission_id>', methods=['DELETE'])
@jwt_required()
def delete_tab_permission(permission_id):
    """Delete a tab permission (Admin only)"""
    try:
        user_id = int(get_jwt_identity())
        
        if not check_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        permission = TabPermission.query.get(permission_id)
        if not permission:
            return jsonify({'error': 'Permission not found'}), 404
        
        db.session.delete(permission)
        db.session.commit()
        
        return jsonify({'message': 'Permission deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
