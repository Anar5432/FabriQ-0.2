import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT name FROM sys.tables WHERE name LIKE '%emp%' OR name LIKE '%per%'"
res = query(sql)
print("Tables with 'emp' or 'per':", [r['name'] for r in res])

sql2 = "SELECT TOP 5 * FROM sm_personal WHERE idn = 7896"
try:
    res2 = query(sql2)
    print("sm_personal:", res2)
except Exception as e:
    print("Error querying sm_personal:", e)
    
sql3 = "SELECT TOP 5 * FROM sm_person WHERE idn = 7896"
try:
    res3 = query(sql3)
    print("sm_person:", res3)
except Exception as e:
    print("Error querying sm_person:", e)
    
sql4 = "SELECT TOP 5 * FROM sm_employee WHERE idn = 7896"
try:
    res4 = query(sql4)
    print("sm_employee:", res4)
except Exception as e:
    print("Error querying sm_employee:", e)

sql5 = "SELECT name FROM sys.tables WHERE name LIKE '%isci%'"
res5 = query(sql5)
print("Tables with 'isci':", [r['name'] for r in res5])
