import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigation_results.txt', 'w', encoding='utf-8') as f:
    
    f.write("=== 1. SEARCHING FOR EXPENSE TABLES ===\n")
    # Query to find tables that might be related to expenses
    sql_tables = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' 
      AND (TABLE_NAME LIKE '%xerc%' 
           OR TABLE_NAME LIKE '%kassa%' 
           OR TABLE_NAME LIKE '%bank%'
           OR TABLE_NAME LIKE '%maas%'
           OR TABLE_NAME LIKE '%emek%')
    """
    tables = query(sql_tables)
    f.write(f"Potential expense/payment tables: {[t['TABLE_NAME'] for t in tables]}\n\n")

    # Let's check sm_xerc if it exists
    if any(t['TABLE_NAME'] == 'sm_xerc' for t in tables):
        try:
            sql_xerc = "SELECT TOP 5 * FROM sm_xerc ORDER BY idn DESC"
            xerc_rows = query(sql_xerc)
            f.write("Recent entries in sm_xerc:\n")
            for r in xerc_rows:
                f.write(f"{r}\n")
            
            # Check if actively used
            sql_xerc_count = "SELECT COUNT(*) as cnt, MAX(tarix) as last_date FROM sm_xerc"
            xc = query(sql_xerc_count)[0]
            f.write(f"\nTotal in sm_xerc: {xc['cnt']}, Last entry: {xc['last_date']}\n\n")
        except Exception as e:
            f.write(f"Error querying sm_xerc: {e}\n\n")

    # Let's look for xerc items in sm_kmd_el or sm_bank_od_el_el (outgoing payments)
    # Actually, sm_kmd_el is incoming or outgoing? 'kmd' = Kassa Mədaxil Orderi (Incoming)
    # 'kmx' = Kassa Məxaric Orderi (Outgoing)
    f.write("=== 2. OUTGOING CASH (sm_kmx) ===\n")
    try:
        sql_kmx = """
        SELECT TOP 10 k.tarix, k.mebleg, k.serh, k.kontra, c.name as kontra_name
        FROM sm_kmx k
        LEFT JOIN sm_kontra c ON k.kontra = c.idn
        ORDER BY k.tarix DESC
        """
        for r in query(sql_kmx):
            f.write(f"{r}\n")
    except Exception as e:
        f.write(f"Error querying sm_kmx: {e}\n")

    f.write("\n=== 3. VENDOR VS CUSTOMER SEPARATION ===\n")
    # Look at sm_kontra columns
    try:
        sql_k_cols = """
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'sm_kontra'
        """
        cols = query(sql_k_cols)
        f.write(f"sm_kontra columns: {[c['COLUMN_NAME'] for c in cols]}\n\n")

        # Let's see if there is a 'tip' or similar
        sql_tip = """
        SELECT tip, COUNT(*) as cnt 
        FROM sm_kontra 
        GROUP BY tip
        """
        try:
            tips = query(sql_tip)
            f.write("sm_kontra 'tip' distribution:\n")
            for t in tips:
                f.write(f"{t}\n")
        except:
            f.write("No 'tip' column found or error.\n")

        # Let's check how many contractors are strictly buyers vs sellers
        sql_buyers_sellers = """
        SELECT 
            SUM(CASE WHEN is_buyer = 1 AND is_seller = 0 THEN 1 ELSE 0 END) as strictly_buyers,
            SUM(CASE WHEN is_buyer = 0 AND is_seller = 1 THEN 1 ELSE 0 END) as strictly_sellers,
            SUM(CASE WHEN is_buyer = 1 AND is_seller = 1 THEN 1 ELSE 0 END) as both,
            SUM(CASE WHEN is_buyer = 0 AND is_seller = 0 THEN 1 ELSE 0 END) as neither
        FROM (
            SELECT 
                k.idn,
                CASE WHEN EXISTS (SELECT 1 FROM sm_kontr_sat WHERE kontra = k.idn) THEN 1 ELSE 0 END as is_buyer,
                CASE WHEN EXISTS (SELECT 1 FROM sm_kontr_al WHERE kontra = k.idn) THEN 1 ELSE 0 END as is_seller
            FROM sm_kontra k
        ) sub
        """
        f.write("\nChecking contractor overlap (based on Sales vs Purchases):\n")
        for r in query(sql_buyers_sellers):
            f.write(f"{r}\n")

    except Exception as e:
        f.write(f"Error in Vendor section: {e}\n")

