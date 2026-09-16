import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
SELECT COUNT(*) as c 
FROM sm_smeta_satis s
JOIN sm_goods g ON s.mal = g.idn
WHERE g.class = 20
"""
res = query(sql)
print(f"SMETA Satis count for class 20: {res}")
