from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # CORS configuration - Allow GitHub Pages and localhost
    CORS(app, 
         resources={r"/api/*": {"origins": [
             "http://localhost:3000",
             "http://localhost:3001",
             "https://kenethdalet21.github.io",
             "https://kdrt0921.pythonanywhere.com"
         ]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Register blueprints
    from app.routes import auth, dashboard, products, inventory, sales, payroll, financial, excel_import_export, settings
    
    app.register_blueprint(auth.bp, url_prefix='/api/v1/auth')
    app.register_blueprint(dashboard.bp, url_prefix='/api/v1/dashboard')
    app.register_blueprint(products.bp, url_prefix='/api/v1/products')
    app.register_blueprint(inventory.bp, url_prefix='/api/v1/inventory')
    app.register_blueprint(sales.bp, url_prefix='/api/v1/sales')
    app.register_blueprint(payroll.bp, url_prefix='/api/v1/payroll')
    app.register_blueprint(financial.bp, url_prefix='/api/v1/financial')
    app.register_blueprint(excel_import_export.excel_bp, url_prefix='/api/v1/excel')
    app.register_blueprint(settings.bp, url_prefix='/api/v1/settings')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Seed default users only if no users exist
        try:
            from app.models import User
            if User.query.count() == 0:
                from app.seed import seed_default_users
                seed_default_users()
        except Exception as e:
            print(f"Note: Could not seed users: {e}")
    
    return app
