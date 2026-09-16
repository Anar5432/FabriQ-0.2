import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
SELECT TOP 10
    'sm_sifaris_form' as source,
    s.idn AS order_id,
    s.sen_no,
    s.tarix
FROM sm_sifaris_form s WITH (NOLOCK)
WHERE s.sen_no IS NULL OR LTRIM(RTRIM(s.sen_no)) = ''

UNION ALL

SELECT TOP 10
    'sm_sif_sened' as source,
    s.idn AS order_id,
    s.sen_no,
    s.tarix
FROM sm_sif_sened s WITH (NOLOCK)
WHERE s.sen_no IS NULL OR LTRIM(RTRIM(s.sen_no)) = ''
"""
try:
    res = query(sql)
    print(f"Total rows found missing sen_no: {len(res)}")
    for r in res:
        print(r)
except Exception as e:
    print(e)
