
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.erp_connector import query

sql = '''
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE COLUMN_NAME = 'idn'
'''
tables = [r['TABLE_NAME'] for r in query(sql)]

for t in tables:
    try:
        sql2 = f'''SELECT TOP 1 '{t}' as t, name FROM {t} WITH (NOLOCK) WHERE idn = 51'''
        res = list(query(sql2))
        for r in res:
            print(r)
    except Exception:
        pass

