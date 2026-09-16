# -*- coding: utf-8 -*-
import sys, os, django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

def deep_research_transfers():
    print("--- DEEP RESEARCH: Transfer Data vs Product Catalog ---")
    
    # Let's pull the 15 most recent transfers from sm_sob_trans_el
    sql = """
        SELECT TOP 15
            t.idn AS transfer_id,
            t.tarix,
            t.serh AS transfer_comment,
            tel.mal AS entered_mal_id,
            g.name AS product_catalog_name,
            tel.miqdar AS qty
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        LEFT JOIN sm_goods g WITH (NOLOCK) ON tel.mal = g.idn
        ORDER BY t.idn DESC
    """
    
    rows = query(sql)
    for r in rows:
        print(f"Transfer: {r['transfer_id']} | Comment: '{r['transfer_comment']}' | Entered ID (mal): {r['entered_mal_id']} | Catalog Name: '{r['product_catalog_name']}' | Qty: {r['qty']}")
        
    print("\n--- Checking if any Order IDs (sif_no) accidentally match Product IDs (mal) ---")
    # Let's see if any active sales order IDs are found in the 'mal' column of transfers
    sql_check = """
        SELECT TOP 5
            s.idn AS order_id,
            s.sen_no AS order_document_number,
            s.kontra_name AS customer,
            t.idn AS transfer_id,
            tel.mal AS transfer_mal
        FROM sm_sif_sened s WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON s.idn = tel.mal
        JOIN sm_sob_trans t WITH (NOLOCK) ON tel.es_no = t.idn
        WHERE s.tarix >= '2025-01-01'
    """
    matches = query(sql_check)
    if matches:
        print("WARNING: Found transfers where the 'mal' (Product ID) exactly matched an Order ID!")
        for m in matches:
            print(m)
    else:
        print("CONFIRMED: The ID entered in the transfer 'mal' column does NOT belong to any recent Order ID. It strictly belongs to the Product Catalog.")

if __name__ == '__main__':
    deep_research_transfers()
