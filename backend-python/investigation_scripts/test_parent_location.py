import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT TOP 1 idn FROM sm_sif_sened WHERE idn = 2675
"""
res = query(sql)
print("Is 2675 in sm_sif_sened?", len(res) > 0)
sql2 = """
    SELECT TOP 1 idn FROM sm_sifaris_form WHERE idn = 2675
"""
res2 = query(sql2)
print("Is 2675 in sm_sifaris_form?", len(res2) > 0)
