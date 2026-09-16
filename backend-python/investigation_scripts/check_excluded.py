import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
SELECT
    s.idn AS order_id,
    s.sen_no
FROM sm_sif_sened s
WHERE s.idn IN (SELECT sifaris FROM sm_sifaris_form WHERE sifaris IS NOT NULL)
"""
try:
    res = query(sql)
    print(f"Total excluded orders: {len(res)}")
    
    missing_number = [r for r in res if not r.get('sen_no') or str(r.get('sen_no')).strip() == '']
    print(f"Excluded orders missing sen_no: {len(missing_number)}")
    
    for r in missing_number:
        print(r)
except Exception as e:
    print(e)
