import sqlite3
import pandas as pd
import great_expectations as gx

def run_data_quality_checks():
    print("Begin Quality Testing (ETL Testing)...\n")
    
    # 1. Connect to the db that we created    
    conn = sqlite3.connect('sales_dwh.db')
    
    # Extract tables for evaluation    
    df_sales = pd.read_sql_query("SELECT * FROM fact_sales", conn)
    df_customers = pd.read_sql_query("SELECT * FROM dim_customers", conn)
    conn.close()

    # 2. Convert normal DataFrames into Great Expectations DataFrames    
    ge_sales = gx.from_pandas(df_sales)
    ge_customers = gx.from_pandas(df_customers)
    
    # 3. Define and execute expectations    
    print("--- Testing: fact_sales ---")
    
    # A. Uniqueness: transaction_id can't be repated    
    res_unique = ge_sales.expect_column_values_to_be_unique(column="transaction_id")
    print(f"[Uniqueness] transaction_id is unique: {'✅ PASS' if res_unique.success else '❌ FAIL'}")
    
    # B. Completeness: There can be no sales without a final amount
    res_not_null = ge_sales.expect_column_values_to_not_be_null(column="final_amount")
    print(f"[Completeness] final_amount has no nulls: {'✅ PASS' if res_not_null.success else '❌ FAIL'}")
    
    # C. Mathematical Validity: Discounts must be logical (between 0% and 50%)
    res_discount = ge_sales.expect_column_values_to_be_between(
        column="discount_applied", 
        min_value=0.0, 
        max_value=0.5
    )
    print(f"[Validity] Discounts between 0 and 0.5: {'✅ PASS' if res_discount.success else '❌ FAIL'}")

    print("\n--- Testing: Referential Integrity ---")
    
    # D. Integrity: All customer_ids in sales must exist in the customer table
    # We obtain the list of valid customers
    valid_customers = ge_customers["customer_id"].tolist()
    res_fk = ge_sales.expect_column_values_to_be_in_set(
        column="customer_id",
        value_set=valid_customers
    )
    print(f"[Integrity] All sales customers exist:: {'✅ PASS' if res_fk.success else '❌ FAIL'}")

    # 4. Final Summary
    all_tests = [res_unique, res_not_null, res_discount, res_fk]
    failed_tests = [test for test in all_tests if not test.success]
    
    print("\n--- ETL TESTING SUMMARY---")
    if len(failed_tests) == 0:
        print("🎉 EXCELLENT! All data quality tests passed. The DWH is ready for BI.")
    else:
        print(f"⚠️ ATTENTION: {len(failed_tests)} test failed. The Data Engineering team must review the pipeline.")

if __name__ == "__main__":
    run_data_quality_checks()