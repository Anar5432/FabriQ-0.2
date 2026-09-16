import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT idn, kontra, kontra_name
    FROM sm_sifaris_form WITH (NOLOCK)
    WHERE idn IN (1863, 2675)
    
    UNION ALL
    
    SELECT idn, kontra, kontra_name
    FROM sm_sif_sened WITH (NOLOCK)
    WHERE idn IN (1863, 2675)
"""
res = query(sql)
print("Historical customer names from the orders themselves:")
for r in res:
    print(r)
