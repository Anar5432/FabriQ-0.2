import os
import sys
import django
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

def default(o):
    return str(o)

sql = "EXEC sp_columns users_oper"
try:
    res = query(sql)
    print("users_oper columns:", [r['COLUMN_NAME'] for r in res])
except Exception as e:
    print("Error:", e)
    
sql2 = "SELECT * FROM users_oper WHERE idn = 7896"
try:
    res2 = query(sql2)
    print("users_oper 7896:", json.dumps(res2, default=default, indent=2))
except Exception as e:
    print("Error:", e)

# There is also a table called 'sm_property1'. What is that? Let's check it.
sql3 = "SELECT name FROM sys.tables WHERE name LIKE '%person%' OR name LIKE '%emp%'"
try:
    res3 = query(sql3)
    print("Tables with person/emp:", [r['name'] for r in res3])
except:
    pass

