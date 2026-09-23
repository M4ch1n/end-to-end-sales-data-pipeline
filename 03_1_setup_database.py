import sqlite3
import os

print("Initializing the Data Warehouse (SQLite)...")

# Name of DB
db_name = 'sales_dwh.db'
sql_script = '03_2_create_dwh_schema.sql'

# Check if the exists
if not os.path.exists(sql_script):
    print(f"❌ Error: File not found {sql_script}.")
    exit()

# Connnect SQLITE
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Read SQL script
with open(sql_script, 'r', encoding='utf-8') as file:
    sql_queries = file.read()

# Execute SQL script
try:
    cursor.executescript(sql_queries)
    conn.commit()
    print("Tables created. (Esquema de Estrella)")
    print(f"Database ready: {db_name}")
except sqlite3.Error as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()

print("Next step: Connect Apache Hop to this db to insert data.")