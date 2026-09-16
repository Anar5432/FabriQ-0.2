import pyodbc
from dashboard.erp_connector import get_connection

def deep_research():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    out = open("research_output.txt", "w", encoding="utf-8")
    
    out.write("=== DEEP RESEARCH ON WAREHOUSE TRANSFERS ===\n")
    
    # 1. Why is Cutting (Kəsim) zero?
    cls = "('5', '6')"
    query_cutting = f"""
    SELECT 
        hm_goods.name AS product_name,
        ins.dept_id,
        ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) AS balance
    FROM sm_goods hm_goods WITH (NOLOCK)
    JOIN sm_goods ym_g WITH (NOLOCK) ON 
        ym_g.class IN {cls} AND (
            hm_goods.idn = ym_g.idn
            OR (ym_g.name LIKE 'YM-%' AND hm_goods.name LIKE 'HM-%'
                AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING(hm_goods.name, 4, LEN(hm_goods.name)))
        )
    JOIN (
        SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        WHERE t.tesdiq = 1 AND t.sobe2 IN (3, 24)
        GROUP BY t.sobe2, tel.mal
    ) ins ON ym_g.idn = ins.mal
    LEFT JOIN (
        SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        WHERE t.tesdiq = 1 AND t.sobe1 IN (3, 24)
        GROUP BY t.sobe1, tel.mal
    ) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
    WHERE hm_goods.class IN {cls}
      AND (ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0)) > 0
    """
    cursor.execute(query_cutting)
    cutting_balances = cursor.fetchall()
    out.write("\n--- Current Balances in Cutting (Dept 3, 24) for HM/YM ---\n")
    if not cutting_balances:
        out.write("  -> ZERO balances found. This is why the dashboard shows 0% for Cutting.\n")
    else:
        for r in cutting_balances:
            out.write(f"  -> {r.product_name} | Dept {r.dept_id} | Balance: {r.balance}\n")

    # 2. Text fields
    out.write("\n--- Checking recent 2026 transfers for hidden order info in text fields ---\n")
    query_text = """
    SELECT TOP 15 
        t.sen_no, 
        t.tarix, 
        t.sobe1, 
        t.sobe2,
        t.serh AS transfer_comment,
        tel.qeyd AS item_note,
        tel.serial AS item_serial,
        tel.sifaris AS item_sifaris,
        g.name AS product_name
    FROM sm_sob_trans t
    JOIN sm_sob_trans_el tel ON t.idn = tel.es_no
    JOIN sm_goods g ON tel.mal = g.idn
    WHERE t.tarix >= '2026-06-01'
    ORDER BY t.idn DESC
    """
    cursor.execute(query_text)
    transfers = cursor.fetchall()
    for t in transfers:
        if t.transfer_comment or t.item_note or t.item_serial or t.item_sifaris:
             out.write(f"Transfer {t.sen_no} | Item: {t.product_name}\n")
             out.write(f"  -> Comment: '{t.transfer_comment}' | Note: '{t.item_note}' | Serial: '{t.item_serial}' | Sifaris_col: '{t.item_sifaris}'\n")
    
    out.write("\n--- Let's do a wider text search on serh and qeyd ---\n")
    query_wide = """
    SELECT TOP 10 t.sen_no, t.tarix, t.serh, tel.qeyd, tel.serial, g.name
    FROM sm_sob_trans t
    JOIN sm_sob_trans_el tel ON t.idn = tel.es_no
    JOIN sm_goods g ON tel.mal = g.idn
    WHERE t.tarix >= '2026-05-01' 
      AND (t.serh IS NOT NULL OR tel.qeyd IS NOT NULL OR tel.serial IS NOT NULL)
      AND (t.serh != '' OR tel.qeyd != '' OR tel.serial != '')
    ORDER BY t.idn DESC
    """
    cursor.execute(query_wide)
    wide_results = cursor.fetchall()
    for w in wide_results:
        out.write(f"{w.sen_no} ({w.tarix}) | Item: {w.name} | Comment: '{w.serh}' | Note: '{w.qeyd}' | Serial: '{w.serial}'\n")

    conn.close()
    out.close()

if __name__ == "__main__":
    deep_research()
