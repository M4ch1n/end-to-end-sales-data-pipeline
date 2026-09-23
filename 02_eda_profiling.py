import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("Starting Exploratory Data Analysis (EDA)...")

# 1. Load the raw data
df_customers = pd.read_csv('raw_customers.csv')
df_products = pd.read_csv('raw_products.csv')
df_sales = pd.read_csv('raw_sales.csv')

# Ensure date columns are parsed as datetime objects
df_sales['date'] = pd.to_datetime(df_sales['date'])
df_customers['signup_date'] = pd.to_datetime(df_customers['signup_date'])

# Set up the visualization style
sns.set_theme(style="whitegrid")

# ==========================================
# PLOT 1: Missing Values (Nulls)
# ==========================================
print("Generating Missing Values plot...")
plt.figure(figsize=(10, 6))
# Calculate percentage of missing values
missing_data = pd.DataFrame({
    'Customers (Email)': [df_customers['email'].isnull().sum() / len(df_customers) * 100],
    'Products (Category)': [df_products['category'].isnull().sum() / len(df_products) * 100],
    'Sales (Quantity)': [df_sales['quantity'].isnull().sum() / len(df_sales) * 100]
})

sns.barplot(data=missing_data)
plt.title('Percentage of Missing Values by Table', fontsize=14)
plt.ylabel('Missing Percentage (%)')
plt.savefig('eda_01_missing_values.png')
plt.close()

# ==========================================
# PLOT 2: Anomalies in Product Prices (Negative values)
# ==========================================
print("Generating Price Distribution plot...")
plt.figure(figsize=(10, 6))
sns.histplot(df_products['base_price'], bins=30, kde=True, color='blue')
# Highlight the negative values
plt.axvspan(-100, 0, color='red', alpha=0.3, label='Data Entry Errors (Negative)')
plt.title('Distribution of Product Base Prices', fontsize=14)
plt.xlabel('Base Price ($)')
plt.ylabel('Count')
plt.legend()
plt.savefig('eda_02_price_anomalies.png')
plt.close()

# ==========================================
# PLOT 3: Future Dates in Sales
# ==========================================
print("Generating Sales Timeline plot...")
plt.figure(figsize=(12, 6))
current_date = datetime.now()

# Aggregate sales by month-year
df_sales['month_year'] = df_sales['date'].dt.to_period('M')
monthly_sales = df_sales.groupby('month_year').size().reset_index(name='transaction_count')
monthly_sales['month_year'] = monthly_sales['month_year'].astype(str)

sns.lineplot(data=monthly_sales, x='month_year', y='transaction_count', marker='o')
plt.axvline(x=current_date.strftime('%Y-%m'), color='red', linestyle='--', label='Current Date')
plt.title('Monthly Sales Transactions (Detecting Future Dates)', fontsize=14)
plt.xticks(rotation=45)
plt.ylabel('Number of Transactions')
plt.legend()
plt.tight_layout()
plt.savefig('eda_03_future_dates.png')
plt.close()

print("EDA complete. Check your folder for the PNG charts.")
print("These charts will be great for the GitHub README!")