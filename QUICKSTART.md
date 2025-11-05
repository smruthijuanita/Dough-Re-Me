# 🚀 Quick Start Guide - PostgreSQL Integration

## ✅ What Was Added

### Complete FastAPI + PostgreSQL Backend Structure

```
app/
├── main.py                 # Main FastAPI app with PostgreSQL
├── api/v1/
│   ├── products.py         # Product CRUD endpoints
│   └── orders.py           # Order management endpoints
├── core/
│   └── config.py           # Database configuration
├── db/
│   ├── base.py            # SQLAlchemy base
│   └── session.py         # Database session
├── models/
│   ├── product.py         # Product model
│   └── order.py           # Order & OrderItem models
└── schemas/
    ├── product.py         # Product validation schemas
    └── order.py           # Order validation schemas

scripts/
├── init_db.py             # Creates database tables
└── seed_db.py             # Adds sample bakery products

Configuration:
├── .env                   # Database credentials (UPDATE THIS!)
├── .env.example          # Template
└── SETUP_POSTGRESQL.md   # Detailed setup guide
```

## 🎯 Next Steps (In Order)

### Step 1: Install PostgreSQL
```powershell
# Download from: https://www.postgresql.org/download/windows/
# Remember your password during installation!
```

### Step 2: Create Database
```powershell
psql -U postgres
CREATE DATABASE dough_re_me;
\q
```

### Step 3: Update .env File
Edit `d:\Dough-Re-Me\.env` and set your PostgreSQL password:
```env
POSTGRES_PASSWORD=your_actual_password
```

### Step 4: Install New Dependencies
```powershell
pip install -r requirements.txt
```

New packages added:
- `psycopg2-binary` - PostgreSQL driver
- `python-dotenv` - Environment variable management
- `email-validator` - Email validation for Pydantic

### Step 5: Initialize Database
```powershell
# Create tables
python scripts\init_db.py

# Add sample products
python scripts\seed_db.py
```

### Step 6: Run the Application
```powershell
# Run the new main app (not serve.py anymore)
python -m app.main
```

## 🌐 Access Points

- **Frontend**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## 🔥 Try the API

### 1. Get All Products
```
GET http://127.0.0.1:8000/api/v1/products
```

### 2. Create a Product
```
POST http://127.0.0.1:8000/api/v1/products
{
  "name": "Red Velvet Cake",
  "description": "Classic red velvet with cream cheese frosting",
  "price": 9.99,
  "category": "cake",
  "image_url": "/static/images/redvelvet.jpeg",
  "in_stock": true
}
```

### 3. Create an Order
```
POST http://127.0.0.1:8000/api/v1/orders
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "555-0123",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

## 📊 Database Tables Created

### Products
- Stores all bakery items
- Fields: name, description, price, category, image_url, in_stock

### Orders
- Customer order information
- Fields: customer details, total_amount, status

### Order Items
- Individual items in each order
- Links products to orders with quantity and price

## 🎨 Frontend Integration

Your existing `index.html` still works! To connect it to the database:

```javascript
// Example: Fetch products from database
fetch('http://127.0.0.1:8000/api/v1/products')
  .then(response => response.json())
  .then(products => {
    console.log('Products from database:', products);
    // Render products dynamically
  });

// Example: Create an order
fetch('http://127.0.0.1:8000/api/v1/orders', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    customer_name: 'Jane Smith',
    customer_email: 'jane@example.com',
    items: [{ product_id: 1, quantity: 2 }]
  })
})
.then(response => response.json())
.then(order => console.log('Order created:', order));
```

## 🔍 Troubleshooting

### Can't connect to database?
1. Check PostgreSQL is running: `pg_ctl status`
2. Verify password in `.env` file
3. Ensure database exists: `psql -U postgres -l`

### Import errors?
Run from project root: `cd D:\Dough-Re-Me`

### Port already in use?
Change port in `app.main` or stop the old server

## 📚 Documentation

- **Detailed Setup**: See `SETUP_POSTGRESQL.md`
- **API Docs**: http://127.0.0.1:8000/docs (interactive!)
- **Database Schema**: Check `SETUP_POSTGRESQL.md`

## 🎉 You're Ready!

You now have:
✅ Complete PostgreSQL database integration
✅ RESTful API with CRUD operations
✅ Automatic API documentation
✅ Sample data seeded
✅ Frontend still working

Start building amazing features! 🥖🍰
