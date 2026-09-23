-- =========================================================
-- Portfolio: Sales Data Warehouse (Star Schema)
-- Database: SQLite
-- =========================================================

-- 1. Clients (Dimension Table)
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    region TEXT,
    signup_date DATE
);

-- 2. Products (Dimension Table)
CREATE TABLE IF NOT EXISTS dim_products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    base_price REAL
);

-- 3. Sales (Fact Table)
CREATE TABLE IF NOT EXISTS fact_sales (
    transaction_id TEXT PRIMARY KEY,
    date DATE NOT NULL,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    discount_applied REAL,
    final_amount REAL, 
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);