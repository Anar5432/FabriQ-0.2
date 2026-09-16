import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT idn, sen_no, tarix, kontra
    FROM sm_sifaris_form WITH (NOLOCK)
    WHERE sen_no LIKE '%2675%' OR sen_no LIKE '%1863%'
    
    UNION ALL
    
    SELECT idn, sen_no, tarix, kontra
    FROM sm_sif_sened WITH (NOLOCK)
    WHERE sen_no LIKE '%2675%' OR sen_no LIKE '%1863%'
"""
res = query(sql)
print("Orders by sen_no:")
for r in res:
    print(r)
