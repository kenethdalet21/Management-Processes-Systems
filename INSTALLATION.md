# Installation and Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 14+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads/)

## Step 1: Clone or Navigate to the Project

If you have the project folder, navigate to it:
```bash
cd "d:\Management Processes Systems"
```

## Step 2: Database Setup

### Windows

1. **Install PostgreSQL** (if not already installed)
   - Download from https://www.postgresql.org/download/windows/
   - Run the installer and remember your password

2. **Create Database**
   ```cmd
   # Open Command Prompt
   cd "C:\Program Files\PostgreSQL\15\bin"
   
   # Create database
   createdb -U postgres business_management_system
   ```

### Mac

1. **Install PostgreSQL**
   ```bash
   brew install postgresql@14
   brew services start postgresql@14
   ```

2. **Create Database**
   ```bash
   createdb business_management_system
   ```

## Step 3: Backend Setup

1. **Navigate to backend folder**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   
   **Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env file and update database credentials
   ```

5. **Initialize database**
   ```bash
   # The database tables will be created automatically on first run
   ```

6. **Run the backend server**
   ```bash
   python run.py
   ```

   The backend should now be running on `http://localhost:5000`

## Step 4: Frontend Setup

1. **Open a new terminal** and navigate to frontend folder
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

   The frontend should now be running on `http://localhost:3000`

## Step 5: Create Initial Admin User

You can create an admin user by making a POST request to the registration endpoint:

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@company.com",
    "password": "Admin123!",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin"
  }'
```

Or use a tool like Postman to send the request.

## Step 6: Login

1. Open your browser and go to `http://localhost:3000`
2. Login with the admin credentials you created
3. Start managing your business!

## Troubleshooting

### Database Connection Issues

**Windows:**
- Ensure PostgreSQL service is running (Services -> postgresql-x64-14)
- Check username and password in `.env` file
- Verify database exists: `psql -U postgres -l`

**Mac:**
- Ensure PostgreSQL is running: `brew services list`
- Check connection: `psql -l`

### Backend Issues

- Ensure virtual environment is activated
- Check all dependencies are installed: `pip list`
- Check Python version: `python --version` (should be 3.11+)

### Frontend Issues

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node version: `node --version` (should be 18+)
- Clear browser cache

### Port Already in Use

**Backend (Port 5000):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac
lsof -ti:5000 | xargs kill -9
```

**Frontend (Port 3000):**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac
lsof -ti:3000 | xargs kill -9
```

## Next Steps

1. Configure business settings in the Settings page
2. Add products/services
3. Set up inventory
4. Start recording sales
5. Generate financial reports

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

## Support

For issues and questions, please refer to the documentation or contact support.
