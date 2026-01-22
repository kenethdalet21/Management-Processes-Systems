# API Reference

## Base URL

```
Development: http://localhost:5000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

All API requests (except login/register) require authentication using JWT tokens.

### Headers

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "admin|operations_manager|finance_manager|employee"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@company.com",
    "role": "admin"
  }
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### Dashboard

#### Get Metrics
```http
GET /dashboard/metrics?year=2030&month=10
```

**Response:**
```json
{
  "all_time": {
    "gross_profit": 2410291.41,
    "sales": 4494741.41,
    "expenses": 2084450.00,
    "gross_profit_margin": 54
  },
  "today": {
    "sales": 17960.00,
    "items_sold": 4,
    "expenses": 19550.00
  },
  "monthly": {
    "items_sold": 277,
    "items_target": 750,
    "items_progress": 37,
    "sales": 380101.16,
    "sales_target": 500000,
    "sales_progress": 76
  }
}
```

#### Get Daily Sales Trend
```http
GET /dashboard/sales-trend/daily?year=2030&month=10
```

#### Get Monthly Sales Trend
```http
GET /dashboard/sales-trend/monthly?year=2030
```

### Products

#### Get All Products
```http
GET /products?page=1&per_page=50&search=&category_id=
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Product 01",
      "sku": "XX-P001",
      "item_cost": 450.00,
      "selling_price": 999.00,
      "profit_margin": 47,
      "current_stock": 25
    }
  ],
  "total": 15,
  "pages": 1,
  "current_page": 1
}
```

#### Get Single Product
```http
GET /products/{id}
```

#### Create Product
```http
POST /products
```

**Request Body:**
```json
{
  "name": "Product Name",
  "sku": "XX-P001",
  "description": "Product description",
  "category_id": 1,
  "item_cost": 450.00,
  "tax_amount": 0.00,
  "other_costs": 80.00,
  "selling_price": 999.00,
  "is_service": false,
  "track_inventory": true,
  "current_stock": 25,
  "low_stock_threshold": 10
}
```

#### Update Product
```http
PUT /products/{id}
```

#### Delete Product
```http
DELETE /products/{id}
```

### Financial

#### Get Income Statement
```http
GET /financial/income-statement?year=2030&month=10
```

**Response:**
```json
{
  "period": {
    "year": 2030,
    "month": 10
  },
  "revenue": 4494741.41,
  "expenses": {
    "breakdown": {
      "General and Administration": 168750.00,
      "Operational Expenses": 204250.00,
      "Marketing & Advertisement": 341440.00
    },
    "total": 2084450.00
  },
  "profit_loss": 2410291.41,
  "profit_margin": 53.63
}
```

#### Get Balance Sheet
```http
GET /financial/balance-sheet?date=2030-10-31
```

**Response:**
```json
{
  "as_of_date": "2030-10-31",
  "assets": {
    "current_assets": 500000.00,
    "fixed_assets": 200000.00,
    "intangible_assets": 50000.00,
    "total": 750000.00
  },
  "liabilities": {
    "current_liabilities": 150000.00,
    "long_term_liabilities": 200000.00,
    "total": 350000.00
  },
  "equity": {
    "total": 400000.00
  },
  "is_balanced": true
}
```

#### Get Cash Flow Statement
```http
GET /financial/cash-flow-statement?year=2030&month=10
```

#### Get Financial Ratios
```http
GET /financial/ratios?year=2030
```

**Response:**
```json
{
  "liquidity": {
    "current_ratio": 3.33,
    "quick_ratio": 2.80
  },
  "leverage": {
    "debt_to_equity": 0.88,
    "debt_ratio": 0.47,
    "interest_coverage": 12.50
  },
  "profitability": {
    "gross_profit_margin": 53.63,
    "net_profit_margin": 48.20,
    "return_on_assets": 24.50,
    "return_on_equity": 56.75
  },
  "efficiency": {
    "asset_turnover": 5.99,
    "inventory_turnover": 8.45,
    "days_sales_outstanding": 35.67
  },
  "market_value": {
    "earnings_per_share": 2.41,
    "price_to_earnings": 15.50
  }
}
```

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "error": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

- Rate limit: 100 requests per minute per IP
- Headers returned:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Pagination

For list endpoints that support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 50, max: 100)

**Response:**
```json
{
  "items": [...],
  "total": 150,
  "pages": 3,
  "current_page": 1
}
```

## Filtering and Search

Most list endpoints support:

**Query Parameters:**
- `search`: Text search
- `sort_by`: Field to sort by
- `order`: `asc` or `desc`
- Additional filters specific to the resource

## Date Formats

All dates should be in ISO 8601 format:
- Date: `YYYY-MM-DD`
- DateTime: `YYYY-MM-DDTHH:mm:ss.sssZ`

## Examples

### Using cURL

```bash
# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!"}'

# Get metrics with token
curl -X GET http://localhost:5000/api/v1/dashboard/metrics \
  -H "Authorization: Bearer <token>"

# Create product
curl -X POST http://localhost:5000/api/v1/products \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"New Product",
    "sku":"XX-P015",
    "item_cost":100.00,
    "selling_price":200.00
  }'
```

### Using JavaScript (Axios)

```javascript
// Login
const loginResponse = await axios.post(
  'http://localhost:5000/api/v1/auth/login',
  { username: 'admin', password: 'Admin123!' }
);

const token = loginResponse.data.access_token;

// Get metrics
const metrics = await axios.get(
  'http://localhost:5000/api/v1/dashboard/metrics',
  { headers: { Authorization: `Bearer ${token}` } }
);

// Create product
const product = await axios.post(
  'http://localhost:5000/api/v1/products',
  {
    name: 'New Product',
    sku: 'XX-P015',
    item_cost: 100.00,
    selling_price: 200.00
  },
  { headers: { Authorization: `Bearer ${token}` } }
);
```

---

For more information, see the main [README.md](README.md).
