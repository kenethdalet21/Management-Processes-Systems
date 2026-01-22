# KDRT Business Management System - Excel Import/Export & Offline Mode

## New Features Implemented

### 1. Excel Import/Export Functionality

All data management pages now support bulk import and export operations using Excel files (.xlsx/.xls format).

#### Available Modules:
- **Product/Service Management** - Import/export products and services
- **Sales Management** - Import/export sales transactions with line items
- **Payroll Management** - Import/export payroll records linked to employees
- **Financial Management** - Export comprehensive financial statements (Income, Balance Sheet, Cash Flow)

#### How to Use:

##### Exporting Data:
1. Navigate to any management page (Products, Sales, Payroll, or Financial)
2. Click the "Export to Excel" button at the top of the page
3. The system will generate an Excel file with all current data
4. File will be downloaded automatically with a timestamp in the filename

##### Importing Data:
1. Click the "Import Excel" button
2. Select an Excel file (.xlsx or .xls)
3. The system will validate and import the data
4. Progress indicators show the import status
5. Success/error messages display the results
6. Errors are tracked row-by-row for easy correction

#### Import Features:
- **SKU-based matching** for products (update existing or create new)
- **Automatic category creation** if categories don't exist
- **Invoice grouping** for sales imports
- **Employee email lookup** for payroll records
- **Comprehensive validation** with detailed error messages
- **Transaction rollback** on critical errors

### 2. Service Management Section

A dedicated section for managing services separately from physical products.

#### Features:
- Separate **Products** and **Services** tabs in Product Management
- Services automatically have inventory tracking disabled
- Different display columns for products vs services
- Pre-configured forms based on selected tab
- Status badges distinguish services from products

#### How to Use:
1. Navigate to Product/Service Management
2. Click the **Services** tab
3. Click "Add Service" to create a new service
4. Services are stored in the same database but flagged as `is_service=true`

### 3. Offline Mode Support

The application now works both online and offline with automatic synchronization.

#### Features:
- **Service Worker** caches static assets and API responses
- **IndexedDB** stores data locally for offline access
- **Automatic sync** when connection is restored
- **Visual indicators** show online/offline status
- **Background sync** queues offline changes for upload

#### How It Works:

##### When Online:
- All operations work normally
- Data is cached in the background for offline use
- API responses are stored in cache

##### When Offline:
- **Orange banner** appears at the top of the screen
- Cached data is used for viewing
- Changes are queued in IndexedDB
- Excel imports are saved locally

##### When Connection Restored:
- **Green notification** shows connection restored
- Background sync automatically uploads pending changes
- Cached data is refreshed with server data
- Users can continue working seamlessly

## Technical Implementation

### Backend (Flask):
- **Excel Processing**: `openpyxl` for writing, `pandas` for data manipulation
- **New Routes**: `/api/v1/excel/` endpoints for each module
- **File Handling**: In-memory BytesIO for efficient file generation
- **Validation**: Row-by-row error tracking with detailed messages

### Frontend (React):
- **ExcelImportExport Component**: Reusable upload/download component
- **File Validation**: Client-side checks for file type
- **Progress Indicators**: Loading states during upload/download
- **Error Display**: User-friendly error messages with details

### Offline Support:
- **Service Worker**: `service-worker.js` in public folder
- **Caching Strategy**: Cache-first for static assets, network-first for API
- **IndexedDB**: Three object stores - `imports`, `pendingSync`, `offlineData`
- **Background Sync**: Automatic upload when connection restored

## API Endpoints

### Products:
- `GET /api/v1/excel/products/export` - Export products to Excel
- `POST /api/v1/excel/products/import` - Import products from Excel

### Sales:
- `GET /api/v1/excel/sales/export` - Export sales with line items
- `POST /api/v1/excel/sales/import` - Import sales transactions

### Payroll:
- `GET /api/v1/excel/payroll/export` - Export payroll records
- `POST /api/v1/excel/payroll/import` - Import payroll data

### Financial:
- `GET /api/v1/excel/financial/export` - Export multi-sheet financial statements

## File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ExcelImportExport.js        # Reusable Excel component
│   │   └── OfflineDetector.js          # Online/offline status detector
│   ├── pages/
│   │   ├── ProductManagement.js        # With Excel & Services tab
│   │   ├── SalesManagement.js          # With Excel import/export
│   │   ├── PayrollManagement.js        # With Excel import/export
│   │   └── FinancialManagement.js      # With Excel export
│   └── index.js                        # Service worker registration
├── public/
│   └── service-worker.js               # Offline caching logic

backend/
└── app/
    └── routes/
        └── excel_import_export.py      # All Excel endpoints
```

## Excel File Formats

### Products Import Template:
| SKU | Name | Description | Category | Item Cost | Tax Amount | Other Costs | Selling Price | Is Service | Track Inventory | Current Stock | Low Stock Threshold |
|-----|------|-------------|----------|-----------|------------|-------------|---------------|------------|-----------------|---------------|---------------------|

### Sales Import Template:
| Invoice Number | Date | Customer Name | Customer Email | Product SKU | Quantity | Unit Price | Notes |
|----------------|------|---------------|----------------|-------------|----------|------------|-------|

### Payroll Import Template:
| Employee Email | Pay Period Start | Pay Period End | Hours Worked | Overtime Hours | Bonus | Deductions | Notes |
|----------------|------------------|----------------|--------------|----------------|-------|------------|-------|

## Currency Format

All monetary values are displayed in **Philippine Peso (₱)** throughout the application.

## Browser Support

- Chrome 80+ (recommended)
- Firefox 75+
- Edge 80+
- Safari 13+

**Note**: Service Worker and IndexedDB are required for offline functionality.

## Development

### Starting the Application:

1. **Backend**:
```bash
cd backend
..\.venv\Scripts\python.exe run.py
```

2. **Frontend**:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Security

- All Excel endpoints are JWT-protected
- File upload validation on both client and server
- SQL injection protection with parameterized queries
- CSRF protection enabled
- Secure file handling with BytesIO (no disk writes)

## Performance

- In-memory file generation (no disk I/O)
- Batch operations for large imports
- Lazy loading for large Excel exports
- IndexedDB for efficient offline storage
- Service Worker caching reduces server load

## Future Enhancements

- Excel template download for each module
- Advanced filtering options for exports
- Scheduled exports (daily/weekly/monthly)
- Import progress tracking with percentage
- Conflict resolution UI for offline sync
- Data compression for large offline datasets

## Support

For issues or questions, please refer to the main README or contact the development team.

---
**Version**: 2.0.0  
**Last Updated**: 2024  
**Platform**: KDRT Business Management System
