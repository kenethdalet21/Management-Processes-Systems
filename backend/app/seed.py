"""
Database seeding script for default users
"""
from app import db, bcrypt
from app.models import User, UserRole


def seed_default_users():
    """Create default users if they don't exist"""
    
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
            'username': 'operations',
            'email': 'operations@kdrt.com',
            'password': 'operations123',
            'first_name': 'Operations',
            'last_name': 'Manager',
            'role': UserRole.OPERATIONS_MANAGER
        },
        {
            'username': 'finance',
            'email': 'finance@kdrt.com',
            'password': 'finance123',
            'first_name': 'Chief Finance',
            'last_name': 'Manager',
            'role': UserRole.FINANCE_MANAGER
        }
    ]
    
    created_users = []
    
    for user_data in default_users:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        
        if not existing_user:
            password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=password_hash,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
            
            db.session.add(user)
            created_users.append(user_data['username'])
    
    if created_users:
        db.session.commit()
        print(f"Created default users: {', '.join(created_users)}")
    else:
        print("All default users already exist")
    
    return created_users
