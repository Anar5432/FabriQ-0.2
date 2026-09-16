import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

print("--- Searching for 61985 in ALL tables ---")
sql_tables = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
tables = [row['TABLE_NAME'] for row in query(sql_tables)]

for table in tables:
    try:
        sql = f"SELECT * FROM {table} WHERE idn = 61985"
        res = query(sql)
        if res:
            print(f"Found ID 61985 in table {table} (column: idn)")
            print(res[0])
    except:
        pass
        
    try:
        sql2 = f"SELECT * FROM {table} WHERE es_no = 61985"
        res2 = query(sql2)
        if res2:
            print(f"Found ID 61985 in table {table} (column: es_no)")
            print(res2[0])
    except:
        pass
