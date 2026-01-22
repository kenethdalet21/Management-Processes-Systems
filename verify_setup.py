#!/usr/bin/env python3
"""
Setup Verification Script for Business Management System
Run this script to verify your installation is correct.
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def check_python_version():
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} is installed")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} found. Python 3.11+ required")
        return False

def check_command(command, name):
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print_success(f"{name} is installed: {result.stdout.strip()}")
            return True
    except Exception as e:
        print_error(f"{name} is not installed or not in PATH")
        return False

def check_node():
    print_header("Checking Node.js")
    return check_command('node', 'Node.js')

def check_npm():
    print_header("Checking npm")
    return check_command('npm', 'npm')

def check_postgres():
    print_header("Checking PostgreSQL")
    commands = ['psql', 'pg_config']
    for cmd in commands:
        if check_command(cmd, 'PostgreSQL'):
            return True
    print_warning("PostgreSQL command line tools not found in PATH")
    print_warning("If PostgreSQL is installed, you may need to add it to PATH")
    return False

def check_directory_structure():
    print_header("Checking Directory Structure")
    
    required_dirs = [
        'backend',
        'backend/app',
        'backend/app/models',
        'backend/app/routes',
        'frontend',
        'frontend/src',
        'frontend/src/pages',
        'frontend/src/components',
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print_success(f"Directory exists: {dir_path}")
        else:
            print_error(f"Directory missing: {dir_path}")
            all_exist = False
    
    return all_exist

def check_required_files():
    print_header("Checking Required Files")
    
    required_files = [
        'backend/requirements.txt',
        'backend/run.py',
        'backend/config.py',
        'backend/.env.example',
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/index.js',
        'README.md',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.isfile(file_path):
            print_success(f"File exists: {file_path}")
        else:
            print_error(f"File missing: {file_path}")
            all_exist = False
    
    return all_exist

def check_env_files():
    print_header("Checking Environment Files")
    
    backend_env = os.path.isfile('backend/.env')
    frontend_env = os.path.isfile('frontend/.env')
    
    if backend_env:
        print_success("Backend .env file exists")
    else:
        print_warning("Backend .env file not found. Copy from .env.example")
    
    if frontend_env:
        print_success("Frontend .env file exists")
    else:
        print_warning("Frontend .env file not found. Copy from .env.example")
    
    return True  # Not critical, just warning

def check_venv():
    print_header("Checking Python Virtual Environment")
    
    venv_paths = ['backend/venv', 'backend/env']
    found = False
    
    for path in venv_paths:
        if os.path.isdir(path):
            print_success(f"Virtual environment found: {path}")
            found = True
            break
    
    if not found:
        print_warning("Virtual environment not found. Create one with: python -m venv venv")
    
    return True  # Not critical

def check_node_modules():
    print_header("Checking Node Modules")
    
    if os.path.isdir('frontend/node_modules'):
        print_success("Node modules installed")
        return True
    else:
        print_warning("Node modules not found. Run: npm install")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║   Business Management System - Setup Verification       ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    checks = {
        "Python Version": check_python_version(),
        "Node.js": check_node(),
        "npm": check_npm(),
        "PostgreSQL": check_postgres(),
        "Directory Structure": check_directory_structure(),
        "Required Files": check_required_files(),
        "Environment Files": check_env_files(),
        "Virtual Environment": check_venv(),
        "Node Modules": check_node_modules(),
    }
    
    print_header("Summary")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print(f"\n{passed}/{total} checks passed\n")
    
    if passed == total:
        print_success("All checks passed! Your setup looks good.")
        print("\nNext steps:")
        print("1. Activate virtual environment (backend/venv)")
        print("2. Install Python dependencies (pip install -r requirements.txt)")
        print("3. Create database (createdb business_management_system)")
        print("4. Start backend (python run.py)")
        print("5. Start frontend (npm start)")
        return 0
    else:
        print_error("Some checks failed. Please review the errors above.")
        print("\nRefer to INSTALLATION.md for detailed setup instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
