import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT * FROM users_oper WHERE idn = 7896 OR emp = 7896 OR per = 7896"
try:
    print("users_oper:", query(sql))
except Exception as e:
    pass
    
sql2 = "SELECT * FROM users_oper WHERE name LIKE '%Ilqar%'"
try:
    print("users_oper search:", query(sql2))
except:
    pass

sql3 = "SELECT * FROM sm_rasenka_emp WHERE idn = 7896"
try:
    print("sm_rasenka_emp:", query(sql3))
except:
    pass
