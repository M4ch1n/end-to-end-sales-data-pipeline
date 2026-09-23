# 📊 End-to-End Sales Data Pipeline & Analytics

## 🎯 Project Overview

This project is a complete, end-to-end data engineering and business intelligence solution simulating a real-world retail environment. The goal of this portfolio project is to demonstrate the ability to extract, transform, and load (ETL) data, handle data quality issues, build a dimensional data warehouse, execute automated ETL tests, and create actionable executive dashboards.

## 🏗️ Architecture & Tech Stack

The data lifecycle follows a modern on-premise to cloud architecture:

1. **Sourcing (Python):** Generated synthetic raw data (Customers, Products, Sales) and injected real-world anomalies (nulls, duplicates, future dates).

2. **Exploratory Data Analysis (Python/Pandas):** Profiling and initial cleansing.

3. **Data Engineering (Apache Hop):** Built ETL pipelines to clean data and conform it into a Star Schema.

4. **Data Warehouse (SQLite):** Stored the transformed data in a dimensional model (Fact and Dimension tables).

5. **Data Quality & ETL Testing (Great Expectations):** Automated validation of business rules, referential integrity, and data types post-load.

6. **Cloud Export (Python):** Flattened the Star Schema into a One Big Table (OBT) for cloud BI consumption.

7. **Business Intelligence (Power BI & Looker Studio):** Semantic modeling (DAX) and UI/UX optimized dashboarding.

**Tools Used:** `Python`, `Pandas`, `Great Expectations`, `Apache Hop`, `SQLite`, `Power BI (DAX)`, `Looker Studio`.

## 📈 Visualizing the Insights

*Note: The dashboards were designed following strict UI/UX best practices, eliminating chart junk and focusing on clear business KPIs.*

### 1. Power BI Executive Dashboard

This dashboard features a complete Star Schema, a custom DAX Date Table for Time Intelligence, and advanced measures like a dynamic Pareto (80/20) calculation.


*(Reemplaza el enlace de arriba con la ruta de tu screenshot de Power BI)*

### 2. Looker Studio Cloud Report

A web-focused dashboard utilizing a One-Big-Table (OBT) architecture, demonstrating cloud deployment capabilities and modern SaaS design.


*(Reemplaza el enlace de arriba con la ruta de tu screenshot de Looker Studio)*

## 📋 Business Questions Answered

Through the semantic models, this project successfully answers:

* **Overall Performance:** What is the Total Revenue, Transaction Volume, and Average Order Value (AOV)?

* **Seasonality:** What does the revenue trend look like over time?

* **Product Performance:** Which categories drive the most revenue?

* **Customer Value (Pareto):** Who are the top 10% of customers generating the bulk of the revenue?

* **Discount Impact:** How do different discount levels affect the Average Order Value?

## 🛠️ Data Quality Handling & Automated Testing

To ensure the integrity of the Data Warehouse, a robust ETL Testing layer was implemented using **Great Expectations**.

The raw data deliberately included several data quality issues (Easter Eggs) to showcase cleansing and testing skills. The automated test suite validates the following dimensions of Data Quality:

* **Uniqueness:** Asserts that primary keys (e.g., `transaction_id`) are never duplicated.

* **Completeness:** Asserts that critical financial columns (e.g., `final_amount`) do not contain `NULL` values.

* **Validity:** Asserts that mathematical rules apply (e.g., `discount_applied` must be strictly between 0% and 50%).

* **Referential Integrity:** Asserts that every `customer_id` present in the Sales Fact table genuinely exists in the Customer Dimension table.

Visual anomalies (like "Null" product categories intentionally left to simulate real-world messy data) were handled directly in the BI Semantic Layer (Looker Studio filter exclusions).

## 🚀 How to Run this Project

1. Run `01_data_generator.py` to generate the raw CSV files.

2. Run `02_eda_profiling.py` to view the data distributions.

3. Run `03_setup_database.py` to create the SQLite Data Warehouse schema.

4. Execute the Apache Hop pipeline to populate the database.

5. **Run `06b_data_quality_tests.py` to execute the Great Expectations test suite and validate the DWH integrity.**

6. Open `07_executive_sales_dashboard.pbix` in Power BI to view the semantic model and report.

7. **Run `08_export_for_looker.py` to generate the `looker_sales_data.csv` (One Big Table).**

8. Upload the generated CSV to Google Drive/Sheets and connect it to Looker Studio to replicate the cloud dashboard.
