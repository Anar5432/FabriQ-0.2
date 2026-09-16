import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

print("--- SEARCHING DATABASE SCHEMA FOR TIME / CAPACITY / NORM METRICS ---")

keywords = [
    'zaman', 'sure', 'vaxt', 'muddet', 'saat', 'deq', 'min', 'time', 'duration',
    'norma', 'kapasite', 'verim', 'eff', 'kadr', 'isci', 'personal', 'marsrut', 
    'emeliyyat', 'oper', 'plan'
]

conditions = " OR ".join([f"c.COLUMN_NAME LIKE '%{k}%' OR t.TABLE_NAME LIKE '%{k}%'" for k in keywords])

sql = f"""
SELECT t.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS c
JOIN INFORMATION_SCHEMA.TABLES t ON c.TABLE_NAME = t.TABLE_NAME
WHERE t.TABLE_TYPE = 'BASE TABLE'
  AND ({conditions})
ORDER BY t.TABLE_NAME, c.COLUMN_NAME;
"""

rows = query(sql)
from collections import defaultdict
tables = defaultdict(list)
for r in rows:
    tables[r['TABLE_NAME']].append(f"{r['COLUMN_NAME']} ({r['DATA_TYPE']})")

for table, cols in tables.items():
    if len(cols) > 0 and 'sm_' in table.lower():
        print(f"\nTable: {table}")
        for c in cols[:10]:
            print(f"  - {c}")
        if len(cols) > 10:
            print(f"  - ... and {len(cols) - 10} more.")
