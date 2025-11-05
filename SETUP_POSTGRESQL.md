# PostgreSQL Database Setup Guide

This guide will help you set up PostgreSQL for the Dough-Re-Me application.

## Quick Start Checklist

- [ ] Install PostgreSQL
- [ ] Create database
- [ ] Configure .env file
- [ ] Install Python dependencies
- [ ] Initialize database tables
- [ ] Seed sample data
- [ ] Run the application

## Detailed Steps

### 1. Install PostgreSQL (Windows)

#### Download and Install
1. Visit https://www.postgresql.org/download/windows/
2. Download the PostgreSQL installer (recommended: version 14 or higher)
3. Run the installer
4. During installation:
   - Remember your **superuser password** (you'll need this!)
   - Default port: **5432** (keep this)
   - Locale: Default
5. Complete the installation

#### Verify Installation
```powershell
# Check PostgreSQL version
psql --version

# Should output something like: psql (PostgreSQL) 14.x
```

### 2. Create Database

#### Option A: Using pgAdmin (GUI)
1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Connect to your local server (enter your password)
3. Right-click **Databases** → **Create** → **Database**
4. Name: `dough_re_me`
5. Click **Save**

#### Option B: Using Command Line
```powershell
# Connect to PostgreSQL
psql -U postgres

# Enter your password when prompted

# Create database
CREATE DATABASE dough_re_me;

# Verify it was created
\l

# Exit psql
\q
```

### 3. Configure Environment Variables

1. Copy the example environment file:
```powershell
cp .env.example .env
```

2. Edit `.env` file with your details:
```env
# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_actual_password_here
POSTGRES_DB=dough_re_me
POSTGRES_PORT=5432

# Application
APP_NAME=Dough-Re-Me Bakery
DEBUG=True
```

**Important**: Replace `your_actual_password_here` with the password you set during PostgreSQL installation!

### 4. Install Python Dependencies

```powershell
# Make sure you're in the project directory
cd D:\Dough-Re-Me

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install all dependencies including PostgreSQL driver
pip install -r requirements.txt
```

Key dependencies installed:
- `psycopg2-binary` - PostgreSQL adapter for Python
- `sqlalchemy` - ORM for database operations
- `fastapi` - Web framework
- `pydantic` - Data validation

### 5. Initialize Database Tables

```powershell
# This creates all tables (products, orders, order_items)
python scripts\init_db.py
```

Expected output:
```
Creating database tables...
✅ Database tables created successfully!
```

### 6. Seed Sample Data (Optional but Recommended)

```powershell
# This adds sample bakery products to your database
python scripts\seed_db.py
```

Expected output:
```
✅ Successfully added 6 products to the database!
```

### 7. Run the Application

```powershell
# Start the server
python -m app.main
```

You should see:
```
🥖 Starting Dough-Re-Me Bakery server with PostgreSQL...
📍 Frontend: http://127.0.0.1:8000
📍 API Docs: http://127.0.0.1:8000/docs
⏹️  Press CTRL+C to stop
```

### 8. Verify Everything Works

1. **Check Health Endpoint**:
   - Open http://127.0.0.1:8000/health
   - Should show: `{"status":"healthy","database":"postgresql"}`

2. **Check API Docs**:
   - Open http://127.0.0.1:8000/docs
   - You'll see interactive API documentation

3. **Test Products Endpoint**:
   - In the API docs, expand `GET /api/v1/products`
   - Click "Try it out" → "Execute"
   - You should see the 6 sample products!

## Database Models

### Products Table
```sql
- id: INTEGER (Primary Key)
- name: VARCHAR(100)
- description: TEXT
- price: FLOAT
- category: VARCHAR(50)
- image_url: VARCHAR(255)
- in_stock: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Orders Table
```sql
- id: INTEGER (Primary Key)
- customer_name: VARCHAR(100)
- customer_email: VARCHAR(100)
- customer_phone: VARCHAR(20)
- total_amount: FLOAT
- status: VARCHAR(20)
- created_at: TIMESTAMP
```

### Order Items Table
```sql
- id: INTEGER (Primary Key)
- order_id: INTEGER (Foreign Key → orders.id)
- product_id: INTEGER (Foreign Key → products.id)
- quantity: INTEGER
- price: FLOAT
```

## Common Issues & Solutions

### Issue: "psql: command not found"
**Solution**: Add PostgreSQL to your PATH:
1. Find your PostgreSQL installation (usually `C:\Program Files\PostgreSQL\14\bin`)
2. Add to System Environment Variables → PATH

### Issue: "password authentication failed"
**Solution**: 
- Make sure the password in `.env` matches your PostgreSQL password
- Try resetting PostgreSQL password:
```powershell
psql -U postgres
ALTER USER postgres PASSWORD 'new_password';
```

### Issue: "database 'dough_re_me' does not exist"
**Solution**: Create it using step 2 above

### Issue: "Port 5432 already in use"
**Solution**: 
- PostgreSQL is already running (this is normal)
- Or another service is using port 5432
- Check with: `netstat -ano | findstr :5432`

### Issue: Import errors when running scripts
**Solution**: 
- Make sure you're running from project root: `cd D:\Dough-Re-Me`
- Use `python -m` prefix: `python -m scripts.init_db`

## Viewing Database Data

### Using pgAdmin
1. Open pgAdmin 4
2. Navigate: Servers → PostgreSQL → Databases → dough_re_me → Schemas → public → Tables
3. Right-click a table → View/Edit Data → All Rows

### Using psql
```powershell
psql -U postgres -d dough_re_me

# List tables
\dt

# View products
SELECT * FROM products;

# View orders
SELECT * FROM orders;

# Count products
SELECT COUNT(*) FROM products;

# Exit
\q
```

## Next Steps

1. **Test the API**: Use the Swagger UI at `/docs` to test creating products and orders
2. **Connect Frontend**: Update your frontend JavaScript to call these API endpoints
3. **Add Authentication**: Implement user authentication for admin features
4. **Set up Migrations**: Use Alembic for database schema versioning
5. **Deploy**: Consider deploying to Heroku, Railway, or Render (they provide free PostgreSQL)

## Need Help?

- PostgreSQL Docs: https://www.postgresql.org/docs/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- FastAPI Docs: https://fastapi.tiangolo.com/

Happy baking! 🥖🍰
