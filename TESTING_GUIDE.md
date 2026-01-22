# 🧪 Complete Testing Guide - KDRT Construction Management System

## 📊 Sample Data Overview

### ✅ Data Successfully Loaded:

- **📦 Products & Services**: 17 items across 5 categories
- **🏢 Customers**: 13 construction companies
- **👥 Employees**: 12 users (1 admin + 11 construction staff)
- **💰 Sales Records**: 150 transactions over 90 days
- **📋 Inventory Logs**: 156 stock movements
- **💵 Payroll Records**: 60 pay periods
- **💼 Total Revenue**: ₱50,561,838.30

---

## 🚀 Getting Started

### Login Credentials:

#### 🔐 Administrator Account:
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: All tabs + Tab Permissions management

#### 👷 Construction Staff Accounts:
All passwords: `password123`

1. **eng_carlos** - Civil Engineering (Operations Manager)
2. **eng_maria** - Structural Engineering (Operations Manager)
3. **sup_juan** - Site Supervision (Operations Manager)
4. **est_anna** - Cost Estimation (Finance Manager)
5. **pm_pedro** - Project Management (Operations Manager)

---

## 📱 Testing Each Module

### 1. 📊 DASHBOARD (Home Page)

**What to Test:**

✅ **Key Metrics Cards:**
- Total Sales Count (150)
- Total Revenue (₱50.5M)
- Low Stock Alerts
- Pending Payments (18)

✅ **Charts & Visualizations:**
- Sales Trend (Last 3 months)
- Revenue by Category
- Top Products by Sales
- Monthly Comparison

✅ **Recent Activity:**
- Recent Sales Transactions
- Low Stock Products
- Recent Payroll Records

**Test Steps:**
1. Login as **admin** / **admin123**
2. View Dashboard homepage
3. Check all metric cards display numbers
4. Verify charts render with data
5. Scroll through recent activity lists
6. Test date range filters if available

**Expected Results:**
- 150 sales transactions visible
- Revenue shows ₱50,561,838.30
- Charts display 3-month trend (Oct-Dec 2025)
- Recent sales list shows latest transactions

---

### 2. 🏗️ PRODUCT/SERVICE LISTING

**What to Test:**

✅ **Product Categories:**
- Building Materials (4 products)
- Steel & Metals (4 products)
- Wood & Timber (3 products)
- Construction Services (2 products)
- Tools & Equipment (4 products)

✅ **CRUD Operations:**
- ➕ Create new product
- ✏️ Edit existing product
- 🗑️ Delete product
- 🔍 Search products
- 📄 Pagination

✅ **Excel Features:**
- 📥 Import products from Excel
- 📤 Export products to Excel
- Bulk operations

**Test Steps:**
1. Navigate to **Product/Service Listing**
2. View all 17 construction products
3. Test search: Search for "Cement"
4. Create new product: "Sand (per cu.m)" - ₱800
5. Edit existing: Change price of Portland Cement
6. Export to Excel (should download .xlsx file)
7. Test bulk delete (select multiple, delete)

**Sample Products to Verify:**
- Portland Cement 50kg bag - ₱280.00
- Ready-Mix Concrete per cu.m - ₱4,500.00
- Steel Rebar #3 (10mm) - ₱45.00
- Marine Plywood 1/2" - ₱850.00

---

### 3. 📦 INVENTORY MANAGEMENT

**What to Test:**

✅ **Inventory Overview:**
- Current stock levels (15 trackable products)
- Low stock alerts
- Stock valuation

✅ **Stock Movements:**
- 86 Stock In movements
- 70 Stock Out movements
- Movement history with dates

✅ **Inventory Logs:**
- View all 156 movements
- Filter by product
- Filter by type (In/Out)
- Date range filtering

**Test Steps:**
1. Navigate to **Inventory Management**
2. View current stock levels for all products
3. Check inventory logs (should show 156 entries)
4. Add new stock movement:
   - Product: Portland Cement
   - Type: Stock In
   - Quantity: 100 bags
   - Notes: "New supplier delivery"
5. Test stock out movement
6. Export inventory report to Excel
7. View low stock alerts

**Expected Data:**
- Multiple PO numbers (Purchase Orders): PO-1000 to PO-9999
- Multiple SO numbers (Sales Orders): SO-1000 to SO-9999
- Date range: Last 60 days of movements

---

### 4. 💰 SALES MANAGEMENT

**What to Test:**

✅ **Sales Overview:**
- 150 total sales records
- 132 paid, 18 pending
- Date range: Oct 26, 2025 - Jan 22, 2026

✅ **Customer Management:**
- 13 construction companies
- Customer purchase history
- Top customers by revenue

✅ **Sales Operations:**
- Create new sale with multiple items
- Edit existing sale
- Mark as paid/pending
- Delete sale
- Filter by date, customer, status

✅ **Sales Analysis:**
- Revenue trends
- Top selling products
- Customer analytics

**Test Steps:**
1. Navigate to **Sales Management**
2. View all 150 sales records
3. Filter by status: "Pending" (should show 18)
4. Create new sale:
   - Customer: Mega Build Corporation
   - Add items: 50 bags Cement, 10 cu.m Concrete
   - Calculate total
   - Save as "Paid"
5. Edit a sale: Change quantity or add item
6. Export sales report to Excel
7. View sales analysis charts

**Sample Customers:**
- Mega Build Corporation
- Skyline Developers Inc.
- Prime Infrastructure Co.
- Golden Gate Builders
- Phoenix Construction Group

---

### 5. 👥 PAYROLL MANAGEMENT

**What to Test:**

✅ **Payroll Records:**
- 60 total payroll records
- Multiple pay periods (6 periods x 10 employees)
- 57 paid, 3 pending

✅ **Payroll Components:**
- Regular hours & pay
- Overtime hours & pay
- Bonuses
- Tax deductions
- Insurance deductions
- Other deductions
- Net pay calculation

✅ **Employee Payroll:**
- Filter by employee
- Filter by pay period
- Filter by paid/unpaid status

**Test Steps:**
1. Navigate to **Payroll Management**
2. View all 60 payroll records
3. Filter by employee: "Carlos Santos"
4. Create new payroll record:
   - Employee: Carlos Santos
   - Period: Last 2 weeks
   - Regular Hours: 160
   - Overtime: 10 hours
   - Calculate automatically
5. Edit existing payroll
6. Mark payroll as paid
7. Export payroll report to Excel
8. View payroll summary by employee

**Sample Data Verification:**
- Regular hours: 80-176 per period
- Overtime hours: 0-25 per period
- Hourly rates: ₱65 - ₱95
- Bonuses: ₱0 - ₱8,000 (occasional)

---

### 6. 💼 FINANCIAL MANAGEMENT

**What to Test:**

✅ **Financial Statements:**
- Income Statement
- Balance Sheet
- Cash Flow Statement

✅ **Financial Ratios:**
- Profitability ratios
- Liquidity ratios
- Efficiency ratios

✅ **Financial Reports:**
- Revenue analysis
- Expense breakdown
- Profit margins
- Period comparisons

**Test Steps:**
1. Navigate to **Financial Management**
2. View financial statements
3. Select date range: Last 3 months
4. Check Income Statement:
   - Total Revenue: ₱50.5M
   - Total Expenses (payroll + others)
   - Net Income/Loss
5. View financial ratios
6. Export financial reports to Excel
7. Compare month-to-month performance

**Expected Metrics:**
- **Dec 2025**: 112 sales, ₱36,587,464.40
- **Nov 2025**: 21 sales, ₱9,837,526.90
- **Oct 2025**: 17 sales, ₱4,136,847.00

---

### 7. ⚙️ SETTINGS (User Profile)

**What to Test:**

✅ **User Profile:**
- View current user info
- Change password
- Update profile details

✅ **System Preferences:**
- Theme settings (if available)
- Notification preferences

**Test Steps:**
1. Navigate to **Settings**
2. View your user profile information
3. Change password:
   - Old password: `admin123`
   - New password: `newpassword123`
   - Confirm new password
   - Save
4. Logout and login with new password
5. Change password back to original

---

### 8. 🔒 TAB PERMISSIONS (Admin Only)

**What to Test:**

✅ **Permission Management:**
- View all non-admin users
- Lock/unlock tabs per user
- Bulk permission updates
- Permission persistence

✅ **Available Tabs to Lock:**
- Products & Services
- Inventory
- Sales
- Payroll
- Financial Reports

**Test Steps:**
1. **Login as admin** (`admin` / `admin123`)
2. Navigate to **Tab Permissions**
3. View list of 12 employees
4. **Test Scenario 1**: Lock Payroll for Operations Manager
   - Find "Carlos Santos" (Operations Manager)
   - Check the "Payroll" checkbox (lock it)
   - Click "Save"
   - Logout
   - Login as `eng_carlos` / `password123`
   - Verify "Payroll Management" is NOT in sidebar
   - Logout

5. **Test Scenario 2**: Lock Multiple Tabs
   - Login as admin again
   - Find "Juan Reyes" (Operations Manager)
   - Lock: Products, Sales, Payroll (3 tabs)
   - Click "Save"
   - Logout
   - Login as `sup_juan` / `password123`
   - Verify only Inventory and Financial are accessible
   - Logout

6. **Test Scenario 3**: Unlock All
   - Login as admin
   - Find any locked user
   - Uncheck all locked tabs
   - Click "Save"
   - Verify user can access all tabs again

**Expected Behavior:**
- Locked tabs disappear from navigation
- User cannot access locked routes even via URL
- Permission changes take effect immediately
- Visual indicators show locked count per user

---

## 🎯 Excel Import/Export Testing

### Products Import/Export:
1. Go to Products tab
2. Click "Export to Excel"
3. Open downloaded file, modify some data
4. Click "Import from Excel"
5. Upload modified file
6. Verify changes applied

### Sales Import/Export:
1. Go to Sales tab
2. Export sales data
3. Verify all 150 records in Excel
4. Test import functionality

### Inventory Import/Export:
1. Go to Inventory tab
2. Export current stock levels
3. Verify all products with quantities
4. Test bulk stock update via import

### Payroll Import/Export:
1. Go to Payroll tab
2. Export payroll records
3. Verify all 60 records with calculations
4. Verify Excel formulas for net pay

---

## 🔍 Bulk Operations Testing

### Bulk Delete Products:
1. Go to Products tab
2. Select multiple products (checkbox)
3. Click "Delete Selected"
4. Confirm deletion
5. Verify products removed

### Bulk Delete Sales:
1. Go to Sales tab
2. Select multiple sales records
3. Click "Delete Selected"
4. Verify deletion

### Bulk Status Update:
1. Select multiple pending sales
2. Mark as "Paid" in bulk
3. Verify status changed

---

## 📊 Dashboard Chart Verification

### Sales Trend Chart:
- **X-axis**: Last 3 months (Oct, Nov, Dec 2025)
- **Y-axis**: Number of sales or revenue
- **Expected**: Upward trend (17 → 21 → 112 sales)

### Revenue by Category Chart:
- Building Materials: Highest revenue
- Steel & Metals: High revenue
- Construction Services: Lower revenue
- Tools & Equipment: Medium revenue

### Top Products Chart:
- Ready-Mix Concrete (highest volume)
- Portland Cement (most frequent)
- Steel Rebar (consistent sales)

---

## ⚡ Performance Testing

### Speed Tests:
1. **Dashboard Load**: Should load under 2 seconds
2. **Product List**: Should load 17 items instantly
3. **Sales List**: Should load 150 records with pagination
4. **Inventory Logs**: Should paginate 156 entries smoothly
5. **Payroll Records**: Should load 60 records quickly

### Pagination Tests:
1. Sales: Test page 1, 2, 3 (10 per page = 15 pages)
2. Inventory Logs: Navigate through pages
3. Products: Test with search + pagination

### Search Performance:
1. Products: Search "cement" (should be instant)
2. Sales: Search by customer name
3. Inventory: Search by product name

---

## 🌐 Offline Mode Testing (If Applicable)

1. Disconnect internet
2. Try to access tabs (should show offline message)
3. Make changes in offline mode
4. Reconnect internet
5. Verify data syncs automatically

---

## 🐛 Error Handling Tests

### Invalid Inputs:
1. Try creating sale with negative quantity
2. Try setting negative price for product
3. Try creating payroll with invalid dates
4. Verify error messages display

### Permission Violations:
1. Try accessing admin-only features as regular user
2. Try accessing locked tabs
3. Verify "Access Denied" messages

### Data Validation:
1. Required fields validation
2. Email format validation
3. Phone number format
4. Date range validation

---

## ✅ Complete Testing Checklist

### Dashboard:
- [ ] View metrics (150 sales, ₱50.5M revenue)
- [ ] Sales trend chart displays
- [ ] Revenue chart displays
- [ ] Low stock alerts visible
- [ ] Recent activity lists populated

### Products:
- [ ] View all 17 products
- [ ] Create new product
- [ ] Edit existing product
- [ ] Delete product
- [ ] Search products
- [ ] Export to Excel
- [ ] Import from Excel

### Inventory:
- [ ] View 156 inventory logs
- [ ] Add stock in movement
- [ ] Add stock out movement
- [ ] Filter by date range
- [ ] Filter by product
- [ ] Export inventory report
- [ ] View low stock alerts

### Sales:
- [ ] View all 150 sales
- [ ] Create new sale
- [ ] Edit sale
- [ ] Delete sale
- [ ] Filter by status (paid/pending)
- [ ] Filter by customer
- [ ] Export sales report
- [ ] View sales analysis

### Payroll:
- [ ] View all 60 payroll records
- [ ] Create new payroll
- [ ] Edit payroll
- [ ] Delete payroll
- [ ] Filter by employee
- [ ] Mark as paid
- [ ] Export payroll report
- [ ] View payroll summary

### Financial:
- [ ] View income statement
- [ ] View balance sheet
- [ ] View cash flow
- [ ] View financial ratios
- [ ] Export financial reports
- [ ] Period comparison

### Tab Permissions:
- [ ] View all users
- [ ] Lock tabs for user
- [ ] Unlock tabs for user
- [ ] Test as locked user
- [ ] Verify tab hiding works
- [ ] Save permissions successfully

---

## 📸 Screenshot Checklist

Take screenshots of:
1. Dashboard with all charts populated
2. Products page showing 17 items
3. Inventory with 156 logs
4. Sales list with 150 records
5. Payroll records table
6. Financial statements
7. Tab Permissions page
8. Successful Excel export
9. Successful Excel import

---

## 🎉 Success Criteria

Your testing is successful if:

✅ All 150 sales display correctly
✅ Dashboard charts show data trends
✅ All CRUD operations work on every tab
✅ Excel import/export functions properly
✅ Bulk operations execute correctly
✅ Tab permissions lock/unlock properly
✅ Locked users cannot access restricted tabs
✅ Data calculations are accurate (totals, net pay, etc.)
✅ Search and filters work correctly
✅ Pagination handles 150+ records smoothly
✅ No console errors in browser developer tools
✅ System is responsive on different screen sizes

---

## 🆘 Troubleshooting

### If Dashboard shows no data:
1. Check browser console for errors
2. Verify backend is running (http://127.0.0.1:5000)
3. Check if data was seeded properly
4. Run: `python enhance_sample_data.py` again

### If charts don't display:
1. Check date range filters
2. Verify sales have dates in last 3 months
3. Refresh browser (Ctrl + F5)
4. Check browser console for errors

### If Excel export fails:
1. Check if `openpyxl` is installed
2. Verify backend logs for errors
3. Try with smaller dataset first

### If Tab Permissions don't work:
1. Verify you're logged in as admin
2. Check if changes saved (green success message)
3. Logout and login as test user
4. Clear browser cache if needed

---

## 📞 Quick Reference

**Backend URL**: http://127.0.0.1:5000
**Frontend URL**: http://localhost:3000

**Admin Login**: `admin` / `admin123`
**Test User**: `eng_carlos` / `password123`

**Data Summary**:
- 150 Sales (₱50.5M)
- 17 Products (5 categories)
- 13 Customers
- 12 Employees
- 60 Payroll Records
- 156 Inventory Movements

---

## 🚀 Ready to Test!

Open your browser to **http://localhost:3000** and start testing!

**Pro Tip**: Open Browser DevTools (F12) to monitor network requests and console logs while testing.

Good luck with your testing! 🎯
