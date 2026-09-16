import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

tables = ['sm_kontra', 'sm_emp', 'users', 'users_oper', 'sm_vetendas', 'sm_person', 'sm_kmd']
for t in tables:
    sql = f"SELECT * FROM {t} WHERE idn = 7896"
    try:
        res = query(sql)
        if res:
            print(f"Found 7896 in {t}:", res)
    except Exception as e:
        pass
        
    try:
        sql2 = f"SELECT * FROM {t} WHERE emp = 7896"
        res2 = query(sql2)
        if res2:
            print(f"Found emp=7896 in {t}:", res2)
    except:
        pass

