import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def explore():
    with open("smeta_satis_out.txt", "w", encoding="utf-8") as f:
        f.write("--- 1. Columns in sm_smeta_satis ---\n")
        sql_cols = """
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'sm_smeta_satis'
        """
        for row in query(sql_cols):
            f.write(f"{row['COLUMN_NAME']}: {row['DATA_TYPE']}\n")

        f.write("\n--- 2. Sample from sm_smeta_satis ---\n")
        sql_sample = "SELECT TOP 3 * FROM sm_smeta_satis ORDER BY idn DESC"
        for row in query(sql_sample):
            f.write(str(row) + "\n")
            
        f.write("\n--- 3. How many active smetas? ---\n")
        sql_count = "SELECT COUNT(*) as cnt FROM sm_smeta WHERE tesdiq = 1"
        res = query(sql_count)
        f.write(f"Count: {res[0]['cnt']}\n")

if __name__ == "__main__":
    explore()
