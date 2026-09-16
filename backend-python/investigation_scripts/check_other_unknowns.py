import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
SELECT TOP 20 
    s.idn AS order_id, 
    s.kontra, 
    c.name,
    c.qeyd,
    c.firma
FROM sm_sif_sened s
LEFT JOIN sm_kontra c ON s.kontra = c.idn
WHERE c.name IS NULL OR LTRIM(RTRIM(c.name)) = ''
AND s.nov IS NULL
AND s.r = 0
ORDER BY s.tarix DESC
"""
try:
    res = query(sql)
    for r in res:
        print(f"Order: {r['order_id']}, Kontra: {r['kontra']}, Name: '{r['name']}', Qeyd: '{r['qeyd']}', Firma: '{r['firma']}'")
except Exception as e:
    print(e)
