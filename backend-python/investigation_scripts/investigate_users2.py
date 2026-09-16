import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "EXEC sp_columns users"
try:
    res = query(sql)
    print("users columns:", [r['COLUMN_NAME'] for r in res])
except Exception as e:
    print("Error:", e)
    
sql2 = "SELECT * FROM users"
try:
    res2 = query(sql2)
    print("\nusers rows:")
    for r in res2:
        print(r)
except Exception as e:
    print("Error:", e)
