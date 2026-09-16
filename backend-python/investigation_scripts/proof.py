import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def get_proof():
    sql = """
    SELECT TOP 5
        CONVERT(VARCHAR(10), t.tarix, 23) as Date,
        t.sobe1 as From_Dept,
        t.sobe2 as To_Dept,
        t.serh as Comment,
        tel.qeyd as Note,
        SUM(tel.miqdar) as Qty
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND t.tarix >= DATEADD(DAY, -60, GETDATE())
      AND ((t.serh IS NOT NULL AND t.serh != '') OR (tel.qeyd IS NOT NULL AND tel.qeyd != ''))
      AND t.sobe2 IN (3, 24)
    GROUP BY CONVERT(VARCHAR(10), t.tarix, 23), t.sobe1, t.sobe2, t.serh, tel.qeyd
    ORDER BY Date DESC
    """
    res = query(sql)
    with open("proof.txt", "w", encoding="utf-8") as f:
        f.write("=== RECENT CUTTING TRANSFERS WITH COMMENTS ===\n")
        for r in res:
            f.write(f"Date: {r['Date']} | From Dept {r['From_Dept']} to Dept {r['To_Dept']} (Cutting) | Comment: '{r['Comment']}' | Note: '{r['Note']}' | Total Qty: {r['Qty']}\n")

if __name__ == "__main__":
    get_proof()
