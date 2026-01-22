import sys
import os

# Add the backend directory to the path
path = '/home/kdrt0921/Management-Processes-Systems/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'kdrt-secret-2026-change-this'
os.environ['JWT_SECRET_KEY'] = 'kdrt-jwt-2026-change-this'

# Change to the backend directory
os.chdir(path)

# Import the Flask app
from run import app as application
