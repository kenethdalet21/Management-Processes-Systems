# User Guide - Business Management System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Dashboard](#dashboard)
3. [Product/Service Management](#productservice-management)
4. [Inventory Management](#inventory-management)
5. [Sales Management](#sales-management)
6. [Payroll Management](#payroll-management)
7. [Financial Management](#financial-management)
8. [Settings](#settings)
9. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### First Login

1. Open your browser and navigate to `http://localhost:3000`
2. Enter your username and password
3. Click **Login**

### Understanding Your Role

Your role determines what you can access:

- **Admin**: Full system access
- **Operations Manager**: Inventory, Sales, Products
- **Finance Manager**: Financial reports, Payroll
- **Employee**: Limited access to assigned areas

---

## Dashboard

The Dashboard is your business command center.

### Key Metrics Cards

**All-time Gross Profit**
- Shows total profit since system start
- Orange card at top left
- Includes profit margin percentage

**All-time Sales**
- Total revenue generated
- Blue card
- Updated with each sale

**Sales Today**
- Today's revenue
- Green card
- Resets daily at midnight

**Items Sold Today**
- Number of items sold today
- Purple card
- Tracks inventory movement

### Charts and Graphs

**Daily Sales Trend**
- Line chart showing sales vs expenses
- Filter by month and year
- Green line = Sales, Red line = Expenses
- Hover for exact values

**Monthly Sales Trend**
- Bar chart showing monthly performance
- Green bars = Sales, Red bars = Expenses
- Compare trends across the year

**Expense Distribution**
- Pie chart showing expense categories
- Click on legend to hide/show categories
- See which areas consume most budget

**Inventory Status**
- Real-time stock levels
- In Stock (Green): Sufficient inventory
- Low Stock (Yellow): Below threshold
- Out of Stock (Red): Needs restocking

### Using Filters

1. Click the **Year** dropdown
2. Select desired year
3. Click the **Month** dropdown
4. Select desired month
5. Dashboard updates automatically

---

## Product/Service Management

### Adding a New Product

1. Click **Product/Service Listing** in sidebar
2. Click **Add Product** button
3. Fill in the form:

   **Basic Information:**
   - Name: Product name
   - SKU: Unique identifier (e.g., XX-P001)
   - Description: Detailed description
   - Category: Select from dropdown

   **Pricing:**
   - Item Cost: Your cost
   - Tax Amount: Tax per unit
   - Other Costs: Additional costs
   - Selling Price: Customer price

   **Inventory:**
   - Track Inventory: Toggle on/off
   - Current Stock: Starting quantity
   - Low Stock Threshold: Alert level

4. Click **Save**

### Editing a Product

1. Find the product in the list
2. Click **Edit** icon
3. Modify the fields
4. Click **Update**

### Product Types

**Physical Products:**
- Track Inventory: ON
- Set stock levels
- Monitor low stock alerts

**Services:**
- Track Inventory: OFF
- No stock tracking needed
- Price-based only

### Profit Margin

The system automatically calculates:
```
Total Cost = Item Cost + Tax + Other Costs
Profit = Selling Price - Total Cost
Profit Margin = (Profit / Selling Price) × 100
```

---

## Inventory Management

### Stock In (Receiving)

1. Go to **Inventory Management**
2. Click **Stock In**
3. Select product
4. Enter quantity received
5. Add date and notes
6. Set status:
   - In Process: Still receiving
   - Completed: Fully received
7. Click **Save**

### Stock Out (Selling/Usage)

1. Click **Stock Out**
2. Select product
3. Enter quantity used
4. Add reason/notes
5. Click **Save**

### Inventory Status

**In Stock** (Green)
- Inventory above threshold
- Safe levels

**Low Stock** (Yellow)
- Below threshold
- Order more soon

**Out of Stock** (Red)
- Zero inventory
- Order immediately

### Inventory Reports

View:
- Current stock levels
- Movement history
- Stock valuation
- Turnover rates

---

## Sales Management

### Creating a Sale

1. Go to **Sales Management**
2. Click **New Sale**
3. **Customer Information:**
   - Select existing customer OR
   - Click **Add New Customer**
   - Fill in customer details

4. **Add Products:**
   - Click **Add Item**
   - Select product
   - Enter quantity
   - Apply discount (optional)
   - Line total calculates automatically

5. **Payment:**
   - Subtotal shows automatically
   - Add discount percentage
   - Tax calculates automatically
   - Review total amount

6. Click **Create Sale**

### Generating Invoices

After creating a sale:
1. Click **Generate Invoice**
2. Review invoice details
3. Options:
   - **Print**: Print directly
   - **Download PDF**: Save to computer
   - **Email**: Send to customer

### Payment Recording

1. Find the sale
2. Click **Record Payment**
3. Enter amount paid
4. Select payment method:
   - Cash
   - Check
   - Card
   - Bank Transfer
5. Add reference number
6. Click **Save**

### Payment Status

- **Pending**: No payment received
- **Partial**: Some payment received
- **Paid**: Fully paid

---

## Payroll Management

### Employee Setup

1. Go to **Payroll Management**
2. Click **Employees**
3. Click **Add Employee**
4. Enter:
   - Personal information
   - Employment type:
     - Hourly (set hourly rate)
     - Salary (set monthly salary)
   - Deductions:
     - Tax rate
     - Insurance
     - Other deductions

### Recording Time

**For Hourly Employees:**
1. Click **Time Entry**
2. Select employee
3. Select pay period
4. Enter:
   - Regular hours
   - Overtime hours
5. System calculates pay:
   - Regular Pay = Hours × Rate
   - Overtime Pay = OT Hours × OT Rate
   - Gross Pay = Regular + Overtime

### Processing Payroll

1. Select pay period
2. Click **Calculate Payroll**
3. Review calculations:
   - Gross pay
   - Deductions
   - Net pay
4. Click **Approve**
5. Mark as **Paid** when payment sent

### Payroll Reports

Generate:
- Individual pay stubs
- Payroll summary
- Tax reports
- Year-to-date reports

---

## Financial Management

### Income Statement

Shows your profitability:

1. Go to **Financial Management**
2. Click **Income Statement**
3. Select period (month/year)
4. View:
   - **Revenue**: Total sales
   - **Expenses**: By category
   - **Profit/Loss**: Net result
   - **Profit Margin**: Percentage

### Balance Sheet

Shows your financial position:

1. Click **Balance Sheet**
2. Select date
3. View:
   - **Assets**:
     - Current (cash, inventory)
     - Fixed (equipment, property)
   - **Liabilities**:
     - Current (short-term debts)
     - Long-term (loans)
   - **Equity**: Owner's stake

The equation: Assets = Liabilities + Equity

### Cash Flow Statement

Shows cash movement:

1. Click **Cash Flow**
2. Select period
3. View:
   - **Operating**: Daily operations
   - **Investing**: Asset purchases
   - **Financing**: Loans, equity

### Financial Ratios

Analyze your business health:

**Liquidity Ratios:**
- **Current Ratio**: Can you pay short-term debts?
  - Good: > 1.5
  - Concerning: < 1.0

- **Quick Ratio**: Can you pay without selling inventory?
  - Good: > 1.0
  - Concerning: < 0.5

**Profitability Ratios:**
- **Gross Profit Margin**: % of revenue after costs
  - Good: > 40%
  - Average: 20-40%

- **ROE (Return on Equity)**: Profit per dollar invested
  - Good: > 15%
  - Average: 10-15%

**Efficiency Ratios:**
- **Inventory Turnover**: How fast you sell inventory
  - Higher is better
  - Industry dependent

- **Asset Turnover**: How efficiently you use assets
  - Higher is better

### Exporting Reports

1. Open any report
2. Click **Export**
3. Choose format:
   - Excel (.xlsx)
   - PDF
   - CSV
4. Download file

---

## Settings

### Business Information

1. Go to **Settings**
2. Click **Business Info**
3. Update:
   - Business name
   - Address
   - Tax ID
   - Contact information
4. Click **Save**

### Financial Settings

**Starting Capital:**
- Enter your initial investment
- Updated automatically with profits

**Fiscal Year:**
- Set your fiscal year start month
- Default: January

**Tax Settings:**
- Default tax rate
- Applies to new sales

### User Management (Admin Only)

**Add Users:**
1. Click **Users**
2. Click **Add User**
3. Enter details
4. Assign role
5. Click **Create**

**Edit Users:**
1. Find user
2. Click **Edit**
3. Change details or role
4. Click **Update**

### Targets and Goals

**Set Monthly Targets:**
1. Click **Targets**
2. Select month/year
3. Enter:
   - Sales target
   - Items sold target
   - Profit target
4. Click **Save**

**Track Progress:**
- Dashboard shows progress bars
- % completion displayed
- Color-coded (red/yellow/green)

---

## Tips & Best Practices

### Daily Tasks

✅ **Morning:**
- Check dashboard metrics
- Review inventory alerts
- Check pending orders

✅ **During Day:**
- Record sales immediately
- Update inventory changes
- Process customer orders

✅ **End of Day:**
- Reconcile cash/payments
- Review day's sales
- Check tomorrow's needs

### Weekly Tasks

✅ **Start of Week:**
- Review weekly targets
- Plan inventory orders
- Schedule staff

✅ **End of Week:**
- Generate sales report
- Review expenses
- Back up data

### Monthly Tasks

✅ **Month End:**
- Close monthly books
- Generate financial statements
- Review financial ratios
- Process payroll
- Analyze performance vs targets

✅ **Month Start:**
- Set new targets
- Review budget
- Plan for month ahead

### Best Practices

**Inventory:**
- Count physical inventory monthly
- Update system immediately
- Set realistic thresholds
- Track slow-moving items

**Sales:**
- Issue invoices promptly
- Follow up on unpaid invoices
- Keep customer data updated
- Track sales trends

**Financial:**
- Categorize expenses correctly
- Record all transactions
- Reconcile accounts monthly
- Review ratios quarterly

**Payroll:**
- Record hours daily
- Process payroll on time
- Keep deductions updated
- Maintain employee records

**Security:**
- Change password regularly
- Use strong passwords
- Log out when done
- Don't share credentials
- Backup data regularly

### Shortcuts and Tips

**Dashboard:**
- Use date filters for comparisons
- Export charts for presentations
- Monitor trends weekly

**Products:**
- Use consistent SKU format
- Update costs regularly
- Review pricing quarterly

**Inventory:**
- Set email alerts for low stock
- Audit inventory monthly
- Track shrinkage

**Sales:**
- Create customer profiles
- Use invoice templates
- Track payment terms

**Reports:**
- Schedule regular reports
- Save favorite filters
- Export for analysis

---

## Getting Help

### Within the System

1. Look for (?) help icons
2. Hover over fields for tips
3. Check validation messages

### Documentation

- [README.md](README.md) - Overview
- [QUICKSTART.md](QUICKSTART.md) - Quick start
- [API_REFERENCE.md](API_REFERENCE.md) - Technical docs

### Support

- Check error messages
- Review user guide
- Contact administrator
- Submit support ticket

---

**Remember:** The system is designed to make your business management easier. Take time to explore features and find what works best for your business!

**Version:** 1.0.0  
**Last Updated:** January 2026
