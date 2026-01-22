# Quick Start Guide

Welcome to the Business Management System! This guide will help you get started quickly.

## 🚀 5-Minute Setup

### 1. Prerequisites Check

Ensure you have installed:
- Python 3.11+ (`python --version`)
- Node.js 18+ (`node --version`)
- PostgreSQL 14+ (Check if running)

### 2. Quick Installation

**Windows PowerShell:**
```powershell
# Navigate to project
cd "d:\Management Processes Systems"

# Setup Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env if needed
python run.py

# In a new terminal - Setup Frontend
cd frontend
npm install
copy .env.example .env
npm start
```

**Mac Terminal:**
```bash
# Navigate to project
cd "/path/to/Management Processes Systems"

# Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py

# In a new terminal - Setup Frontend
cd frontend
npm install
cp .env.example .env
npm start
```

### 3. Create Admin User

Open a new terminal and run:

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

### 4. Login

1. Open browser: `http://localhost:3000`
2. Login with:
   - Username: `admin`
   - Password: `Admin123!`

## 📊 First Steps

### 1. Configure Business Settings

1. Click **Settings** in sidebar
2. Enter your:
   - Business Name
   - Tax ID
   - Address
   - Starting Capital

### 2. Add Products/Services

1. Go to **Product/Service Listing**
2. Click **Add Product**
3. Fill in:
   - Name
   - SKU
   - Cost
   - Selling Price
   - Category

### 3. Record Your First Sale

1. Go to **Sales Management**
2. Click **New Sale**
3. Select customer
4. Add products
5. Generate invoice

### 4. View Dashboard

Go to **Dashboard** to see:
- Real-time metrics
- Sales trends
- Inventory status
- Financial overview

## 🎯 Key Features Overview

### Dashboard
- **All-time metrics**: Gross profit, sales, expenses
- **Daily tracking**: Today's sales and items sold
- **Trends**: Daily and monthly sales charts
- **Inventory**: Real-time stock status

### Product Management
- Add/Edit/Delete products and services
- Track costs, pricing, and profit margins
- Categorize products
- Manage SKUs

### Inventory Management
- Stock-in/Stock-out logging
- Real-time inventory levels
- Low stock alerts
- Inventory analysis

### Sales Management
- Create sales orders
- Generate professional invoices
- Track customer information
- Record payments
- Sales reporting

### Payroll Management
- Employee time tracking
- Hourly and salary-based pay
- Calculate deductions
- Generate payroll reports
- Payment history

### Financial Management

**Financial Statements:**
- Income Statement
- Balance Sheet
- Cash Flow Statement

**Financial Ratios:**
- Liquidity: Current Ratio, Quick Ratio
- Leverage: Debt-to-Equity, Interest Coverage
- Profitability: Gross Margin, ROE, ROA
- Efficiency: Asset Turnover, Inventory Turnover
- Market Value: P/E Ratio, EPS (for public companies)

## 👥 User Roles

### Admin
- Full system access
- User management
- All modules

### Operations Manager
- Inventory Management ✅
- Sales Management ✅
- Product Management ✅
- Dashboard (Read-only)

### Finance Manager
- Financial Management ✅
- Payroll Management ✅
- Dashboard (Read-only)
- Reports access

### Employee
- Limited access
- Own time tracking
- Assigned reports

## 💡 Tips

1. **Regular Backups**: Export data regularly
2. **Update Targets**: Set monthly targets in settings
3. **Monitor Inventory**: Check low stock alerts daily
4. **Review Reports**: Generate financial reports monthly
5. **User Training**: Train staff on their specific modules

## 🔧 Common Tasks

### Export Reports to Excel

1. Navigate to any report page
2. Click **Export** button
3. Select Excel format
4. Download file

### Generate Invoice

1. Go to Sales Management
2. Create new sale
3. Click **Generate Invoice**
4. Print or download PDF

### Add New Employee

1. Go to Settings
2. Click **Users**
3. Add new user with role
4. Set up payroll information

### Check Financial Ratios

1. Go to Financial Management
2. Click **Financial Ratios**
3. View all ratio calculations
4. Export for analysis

## 📱 Access Options

### Web Browser
- Access from any device
- URL: `http://localhost:3000` (development)
- Production: Your domain

### Desktop App
- Download from releases
- Install on Windows/Mac
- Offline capable

### Mobile
- Responsive web interface
- Works on tablets and phones

## 🆘 Getting Help

### Documentation
- [README.md](README.md) - Full documentation
- [INSTALLATION.md](INSTALLATION.md) - Detailed setup
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

### Troubleshooting
See [INSTALLATION.md](INSTALLATION.md) troubleshooting section

### Support
- Check documentation
- Review error logs
- Contact support team

## 🎓 Video Tutorials

Coming soon:
- System overview
- Adding products
- Recording sales
- Generating reports
- Financial analysis

## 📈 Next Steps

1. ✅ Complete initial setup
2. ✅ Add your products/services
3. ✅ Set up inventory
4. ✅ Record some sales
5. ✅ Add employees
6. ✅ Generate first report
7. ✅ Configure automated backups
8. ✅ Train your team

---

**Congratulations!** You're now ready to manage your business efficiently with BMS.

For detailed information on any feature, refer to the full documentation in [README.md](README.md).
