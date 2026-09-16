import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def check_where_materials_are():
    sql_req = """
    SELECT 
        DISTINCT xammal.mal AS raw_material_id
    FROM sm_smeta_satis satis WITH (NOLOCK)
    JOIN (
        SELECT mal, MAX(es_no) as latest_smeta_id
        FROM sm_smeta_satis s WITH (NOLOCK)
        JOIN sm_smeta sm WITH (NOLOCK) ON s.es_no = sm.idn
        WHERE sm.tesdiq = 1
        GROUP BY mal
    ) latest ON satis.mal = latest.mal AND satis.es_no = latest.latest_smeta_id
    JOIN sm_smeta_xammal xammal WITH (NOLOCK) ON satis.es_no = xammal.es_no
    """
    req_raw = query(sql_req)
    all_needed_materials = [str(r['raw_material_id']) for r in req_raw]
    mat_list = ",".join(all_needed_materials)

    sql = f"""
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
            WHERE t.tesdiq = 1 AND tel.mal IN ({mat_list})
            GROUP BY t.sobe2, tel.mal
        ) ins
        FULL OUTER JOIN (
            SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
            FROM sm_sob_trans t WITH (NOLOCK)
            JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
            WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL AND tel.mal IN ({mat_list})
            GROUP BY t.sobe1, tel.mal
        ) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
    ) bal
    WHERE balance > 0
    GROUP BY dept_id
    ORDER BY total_qty DESC
    """
    bals = query(sql)
    for b in bals:
        print(f"Dept {b['dept_id']}: {b['material_count']} distinct materials, {b['total_qty']} total qty")

if __name__ == "__main__":
    check_where_materials_are()
