import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import query

sql = """
SELECT TOP 20 s.tarix, s.sen_no, k.name as customer, g.name as product, e.miqdar, g.class
FROM sm_sifaris_form s 
JOIN sm_sifaris_form_el e ON s.idn = e.es_no 
JOIN sm_goods g ON e.mal = g.idn 
JOIN sm_kontra k ON s.kontra = k.idn 
WHERE k.name LIKE '%AZƏRSU%' OR k.name LIKE '%BAKU ELEC%' OR k.name LIKE '%MİLLA%'
ORDER BY s.tarix DESC
"""
rows = query(sql)
print("--- SIFARIS FORM ORDERS ---")
for r in rows:
    print(f"Date: {r['tarix']} | Order: {r['sen_no']} | Cust: {r['customer'].encode('ascii', 'ignore').decode()} | Prod: {r['product'].encode('ascii', 'ignore').decode()} | Qty: {r['miqdar']} | Class: {r['class']}")

sql2 = """
SELECT TOP 20 s.tarix, s.sen_no, k.name as customer, g.name as product, e.miqdar, g.class
FROM sm_sif_sened s 
JOIN sm_sif_sened_el e ON s.idn = e.es_no 
JOIN sm_goods g ON e.mal = g.idn 
JOIN sm_kontra k ON s.kontra = k.idn 
WHERE k.name LIKE '%KURORT%' OR k.name LIKE '%BAKU ELEC%' OR k.name LIKE '%MİLLA%'
ORDER BY s.tarix DESC
"""
rows2 = query(sql2)
print("\n--- SIF SENED ORDERS ---")
for r in rows2:
    print(f"Date: {r['tarix']} | Order: {r['sen_no']} | Cust: {r['customer'].encode('ascii', 'ignore').decode()} | Prod: {r['product'].encode('ascii', 'ignore').decode()} | Qty: {r['miqdar']} | Class: {r['class']}")

