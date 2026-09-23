import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_SALES = 5000

print("Starting Data Generation...")

# ==========================================
# 1. GENERATE CUSTOMERS
# ==========================================
print("Generating Customers data...")
customers = []
regions = ['North America', 'Europe', 'Asia', 'Latin America', 'Middle East']

for _ in range(NUM_CUSTOMERS):
    customers.append({
        'customer_id': fake.unique.random_int(min=1000, max=9999),
        'full_name': fake.name(),
        'email': fake.email(),
        'region': random.choice(regions),
        'signup_date': fake.date_between(start_date='-3y', end_date='today')
    })

df_customers = pd.DataFrame(customers)

# Inject Anomalies into Customers
# - Null emails (5%)
df_customers.loc[df_customers.sample(frac=0.05).index, 'email'] = np.nan
# - Duplicate a few rows (simulate system glitch)
df_customers = pd.concat([df_customers, df_customers.sample(n=10)], ignore_index=True)


# ==========================================
# 2. GENERATE PRODUCTS
# ==========================================
print("Generating Products data...")
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys']
products = []

for _ in range(NUM_PRODUCTS):
    products.append({
        'product_id': fake.unique.random_int(min=100, max=999),
        'product_name': fake.catch_phrase(),
        'category': random.choice(categories),
        'base_price': round(random.uniform(10.0, 500.0), 2)
    })

df_products = pd.DataFrame(products)

# Inject Anomalies into Products
# - Negative prices (Data entry error)
df_products.loc[df_products.sample(n=3).index, 'base_price'] *= -1
# - Null category
df_products.loc[df_products.sample(n=2).index, 'category'] = np.nan


# ==========================================
# 3. GENERATE SALES (TRANSACTIONS)
# ==========================================
print("Generating Sales data...")
sales = []
customer_ids = df_customers['customer_id'].dropna().unique().tolist()
product_ids = df_products['product_id'].dropna().unique().tolist()

for _ in range(NUM_SALES):
    sales.append({
        'transaction_id': fake.unique.uuid4(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'customer_id': random.choice(customer_ids),
        'product_id': random.choice(product_ids),
        'quantity': random.randint(1, 10),
        'discount_applied': round(random.uniform(0.0, 0.3), 2) # 0% to 30% discount
    })

df_sales = pd.DataFrame(sales)

# Inject Anomalies into Sales
# - Dates in the future (Timezone/System error)
future_date = datetime.now() + timedelta(days=30)
df_sales.loc[df_sales.sample(n=15).index, 'date'] = future_date
# - Null quantities
df_sales.loc[df_sales.sample(frac=0.02).index, 'quantity'] = np.nan
# - Orphan records (Customer ID that doesn't exist in Customer table)
df_sales.loc[df_sales.sample(n=20).index, 'customer_id'] = 99999


# ==========================================
# 4. EXPORT TO CSV
# ==========================================
print("Exporting to CSV files...")
df_customers.to_csv('raw_customers.csv', index=False)
df_products.to_csv('raw_products.csv', index=False)
df_sales.to_csv('raw_sales.csv', index=False)

print("Data generation complete. Check your folder for the raw CSV files.")

# Quick EDA Summary
print("\n--- DATA QUALITY REPORT (EDA Preview) ---")
print(f"Total Sales Records: {len(df_sales)}")
print(f"Null quantities found: {df_sales['quantity'].isnull().sum()}")
print(f"Future dates found: {(df_sales['date'] > datetime.now()).sum()}")
print(f"Negative product prices found: {(df_products['base_price'] < 0).sum()}")
print(f"Missing customer emails: {df_customers['email'].isnull().sum()}")
print(f"Duplicate customer records: {df_customers.duplicated().sum()}")