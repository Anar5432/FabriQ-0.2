import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "EXEC sp_columns sm_sif_sened"
res = query(sql)
for r in res:
    print(r['COLUMN_NAME'], r['TYPE_NAME'])
