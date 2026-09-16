import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def check_depts():
    with open("depts_out.txt", "w", encoding="utf-8") as f:
        f.write("--- Departments ---\n")
        depts = query("SELECT idn, name FROM sm_depo")
        for d in depts:
            f.write(f"Dept {d['idn']}: {d['name']}\n")

        f.write("\n--- Raw Material Balances by Dept ---\n")
        sql = """
        SELECT 
            dept_id,
            COUNT(mal) as material_count,
            SUM(balance) as total_qty
        FROM (
            SELECT 
                ISNULL(ins.dept_id, outs.dept_id) as dept_id,
                ISNULL(ins.mal, outs.mal) as mal,
                ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) as balance
            FROM (
                SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in
                FROM sm_sob_trans t WITH (NOLOCK)
                JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
                JOIN sm_goods g WITH (NOLOCK) ON tel.mal = g.idn
                WHERE t.tesdiq = 1 AND g.class IN (1, 2, 22) -- Xammal classes?
                GROUP BY t.sobe2, tel.mal
            ) ins
            FULL OUTER JOIN (
                SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
                FROM sm_sob_trans t WITH (NOLOCK)
                JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
                JOIN sm_goods g WITH (NOLOCK) ON tel.mal = g.idn
                WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL AND g.class IN (1, 2, 22)
                GROUP BY t.sobe1, tel.mal
            ) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
        ) bal
        WHERE balance > 0
        GROUP BY dept_id
        ORDER BY total_qty DESC
        """
        bals = query(sql)
        for b in bals:
            f.write(f"Dept {b['dept_id']}: {b['material_count']} distinct materials, {b['total_qty']} total qty\n")

if __name__ == "__main__":
    check_depts()
