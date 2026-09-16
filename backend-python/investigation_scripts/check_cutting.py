import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def verify_cutting():
    sql = """
    SELECT 
        t.sobe2 AS dest_dept, 
        SUM(tel.miqdar) AS total_qty,
        COUNT(*) AS transaction_count
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND t.tarix >= DATEADD(DAY, -60, GETDATE())
      AND ((t.serh IS NOT NULL AND t.serh != '') OR (tel.qeyd IS NOT NULL AND tel.qeyd != ''))
    GROUP BY t.sobe2
    ORDER BY total_qty DESC
    """
    res = query(sql)
    print("=== Transfers in the last 60 days that have COMMENTS ===")
    for row in res:
        print(f"Destination Dept {row['dest_dept']}: {row['total_qty']} items (across {row['transaction_count']} transactions)")

if __name__ == "__main__":
    verify_cutting()
