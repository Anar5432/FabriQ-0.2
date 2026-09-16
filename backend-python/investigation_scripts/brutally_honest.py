import pyodbc
from dashboard.erp_connector import get_connection

def brutally_honest_investigation():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    
    print("=== BRUTALLY HONEST DASHBOARD ANALYSIS ===")
    
    # 1. Let's check what 'cls' is for the dashboard
    cls = "('5', '6')" # Class 5 is HM (Finished), Class 6 is YM (Half-Finished)
    
    # 2. Are there any items in Dept 8 or 9 (Material Warehouse stage) that match active orders?
    query = f"""
    SELECT 
        hm_goods.idn AS hm_mal,
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
        WHERE t.tesdiq = 1 AND t.sobe2 IN (8, 9)
        GROUP BY t.sobe2, tel.mal
    ) ins ON ym_g.idn = ins.mal
    LEFT JOIN (
        SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL AND t.sobe1 IN (8, 9)
        GROUP BY t.sobe1, tel.mal
    ) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
    WHERE hm_goods.class IN {cls}
      AND (ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0)) > 0
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"\nItems in Dept 8 or 9 (Dashboard Stage: Ambar Material) with balance > 0:")
    if not results:
        print("  -> ZERO ITEMS FOUND! This is why the dashboard shows 0.")
    else:
        for r in results:
            print(f"  -> {r.product_name} (ID: {r.hm_mal}) | Dept: {r.dept_id} | Balance: {r.balance}")

    # 3. What about Raw Materials (Class 1 or 2)?
    print("\n--- Why didn't the June 13th transaction show up on the dashboard? ---")
    query_june13 = """
    SELECT TOP 5 t.sen_no, t.tarix, tel.kod, tel.mal, g.name, g.class, t.sobe1, t.sobe2
    FROM sm_sob_trans t
    JOIN sm_sob_trans_el tel ON t.idn = tel.es_no
    JOIN sm_goods g ON tel.mal = g.idn
    WHERE t.sen_no = '046777' OR t.tarix >= '2026-06-13'
    ORDER BY t.idn DESC
    """
    cursor.execute(query_june13)
    transactions = cursor.fetchall()
    for t in transactions:
         print(f"Transaction: {t.sen_no} | Item: {t.name} | Class: {getattr(t, 'class')} | From: {t.sobe1} -> To: {t.sobe2}")
         
    conn.close()

if __name__ == "__main__":
    brutally_honest_investigation()
