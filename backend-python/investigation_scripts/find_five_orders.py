import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

def get_columns(table):
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
    return [r[0] for r in cursor.fetchall()]

query = """
SELECT TOP 5 s.idn as smeta_id, s.tarix, s.is_ad as ad, sm.mal, g.name as product_name
FROM sm_smeta s
JOIN sm_smeta_mal sm ON s.idn = sm.es_no
JOIN sm_goods g ON sm.mal = g.idn
WHERE EXISTS (SELECT 1 FROM sm_smeta_xammal WHERE es_no = s.idn)
  AND (EXISTS (SELECT 1 FROM sm_smeta_xidmet WHERE es_no = s.idn) OR EXISTS (SELECT 1 FROM sm_smeta_naxis WHERE es_no = s.idn) OR EXISTS (SELECT 1 FROM sm_smeta_xerc WHERE es_no = s.idn))
ORDER BY s.tarix DESC
"""
cursor.execute(query)
columns = [column[0] for column in cursor.description]
smetas = [dict(zip(columns, row)) for row in cursor.fetchall()]

with codecs.open('final_research.txt', 'w', 'utf-8') as out:
    out.write("--- 5 RECENT SMETA (BOM) RECORDS ---\n")
    for s in smetas:
        out.write(f"\nSmeta ID: {s['smeta_id']} | Date: {s['tarix']} | Name: {s['ad']}\n")
        out.write(f"Product: {s['product_name']} (ID: {s['mal']})\n")
        
        # Check if there is a sifaris_form order for this product
        cur2 = conn.cursor()
        cur2.execute("SELECT TOP 1 f.idn, f.sen_no FROM sm_sifaris_form f JOIN sm_sifaris_el e ON f.idn = e.es_no WHERE e.mal = %d ORDER BY f.tarix DESC", (s['mal'],))
        order = cur2.fetchone()
        if order:
            out.write(f"  Associated Order: {order[1]} (IDN: {order[0]})\n")
        else:
            out.write(f"  Associated Order: None found in sm_sifaris_form\n")
            
        # Materials
        cur2.execute("SELECT x.mal, g.name, x.miqdar FROM sm_smeta_xammal x JOIN sm_goods g ON x.mal = g.idn WHERE x.es_no = %d", (s['smeta_id'],))
        mats = cur2.fetchall()
        out.write("  Materials required (Raw center document):\n")
        for m in mats:
            out.write(f"    - {m[1]} (Qty: {m[2]})\n")
            
        # Stages from sm_smeta_xidmet
        cur2.execute("SELECT * FROM sm_smeta_xidmet WHERE es_no = %d", (s['smeta_id'],))
        xidmet = cur2.fetchall()
        
        # Get column names for xidmet
        columns_x = [column[0] for column in cur2.description]
        out.write("  Production Stages (sm_smeta_xidmet):\n")
        for x in xidmet:
            out.write(f"    - Stage: {dict(zip(columns_x, x))}\n")
            
        # Try sm_smeta_naxis
        cur2.execute("SELECT * FROM sm_smeta_naxis WHERE es_no = %d", (s['smeta_id'],))
        naxis = cur2.fetchall()
        columns_n = [column[0] for column in cur2.description]
        if naxis:
            out.write("  Naxis (Embroidery):\n")
            for n in naxis:
                out.write(f"    - {dict(zip(columns_n, n))}\n")

conn.close()
