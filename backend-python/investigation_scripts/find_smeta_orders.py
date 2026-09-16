import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

import pyodbc
from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

# Get recent sm_smeta that have a sifaris link
query_smeta = """
SELECT TOP 20 s.idn, s.num, s.ad, s.sifaris, s.tarix, s.mal,
       (SELECT name FROM sm_goods WHERE idn = s.mal) as product_name
FROM sm_smeta s
WHERE s.sifaris IS NOT NULL AND s.sifaris > 0
ORDER BY s.tarix DESC
"""
cursor.execute(query_smeta)
smetas = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

with codecs.open('smeta_orders_test.txt', 'w', 'utf-8') as f:
    for s in smetas:
        f.write(f"Smeta: {s}\n")
        
        # materials
        cur2 = conn.cursor()
        cur2.execute("SELECT x.mal, g.name, x.miqdar FROM sm_smeta_xammal x JOIN sm_goods g ON x.mal = g.idn WHERE x.es_no = ?", (s['idn'],))
        mats = cur2.fetchall()
        for m in mats:
            f.write(f"   Material: {m[1]} ({m[2]})\n")
            
        # check if there is a stages table
        cur2.execute("SELECT name FROM sys.tables WHERE name LIKE '%smeta%' OR name LIKE '%faza%' OR name LIKE '%emel%' OR name LIKE '%marh%' OR name LIKE '%rasc%' OR name LIKE '%rasenk%'")
        tables = [r[0] for r in cur2.fetchall()]
        f.write(f"   Possible stage tables: {tables}\n")
        
        # Try to find production stages for this smeta
        # "sm_rasc" or "sm_smeta_emek" maybe?
        if 'sm_smeta_emek' in tables:
            cur2.execute("SELECT * FROM sm_smeta_emek WHERE es_no = ?", (s['idn'],))
            emek = cur2.fetchall()
            for em in emek:
                f.write(f"   Emek stage: {em}\n")
                
        if 'sm_rasc' in tables:
            cur2.execute("SELECT * FROM sm_rasc WHERE mal = ?", (s['mal'],))
            rasc = cur2.fetchall()
            for r in rasc:
                f.write(f"   Rasc (stage): {r}\n")
                
        # What about sm_sifaris_form for status?
        cur2.execute("SELECT status, status_ad FROM sm_sifaris_form WHERE idn = ?", (s['sifaris'],))
        sif = cur2.fetchall()
        f.write(f"   Order Status: {sif}\n")

        break

conn.close()
