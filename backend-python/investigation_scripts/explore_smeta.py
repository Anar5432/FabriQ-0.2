import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def explore_smeta():
    print("--- 1. Columns in sm_smeta ---")
    sql_cols = """
    SELECT COLUMN_NAME, DATA_TYPE 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'sm_smeta'
    """
    for row in query(sql_cols):
        print(f"{row['COLUMN_NAME']}: {row['DATA_TYPE']}")

    print("\n--- 2. Sample from sm_smeta ---")
    sql_sample = "SELECT TOP 3 * FROM sm_smeta ORDER BY idn DESC"
    for row in query(sql_sample):
        print(row)

if __name__ == "__main__":
    explore_smeta()
