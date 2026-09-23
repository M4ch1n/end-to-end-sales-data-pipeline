import sqlite3
import pandas as pd
import os

print("Preparing data for the cloud (Looker Studio)...")

db_name = 'sales_dwh.db'
output_csv = 'looker_sales_data.csv'

if not os.path.exists(db_name):
    print(f"❌ Error: No se encontró {db_name}.")
    exit()

# Connect to db
conn = sqlite3.connect(db_name)

# SQL query to join the Star Schema into one big table (OBT)
query = """
SELECT 
    f.transaction_id,
    f.date,
    c.full_name AS customer_name,
    c.email,
    c.region,
    p.product_name,
    p.category,
    f.quantity,
    f.discount_applied,
    f.final_amount
FROM fact_sales f
LEFT JOIN dim_customers c ON f.customer_id = c.customer_id
LEFT JOIN dim_products p ON f.product_id = p.product_id
"""

print("Executing join...")
# Leer usando Pandas y exportar a CSV
df = pd.read_sql_query(query, conn)
df.to_csv(output_csv, index=False)

conn.close()
print(f"Export successful! File created: {output_csv}")
print("Next step: upload this file to Google Drive (Google Sheets) to connect to Looker Studio.")