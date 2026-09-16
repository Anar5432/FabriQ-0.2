import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT idn, sen_no, tarix, kontra, sifaris
    FROM sm_sifaris_form WITH (NOLOCK)
    WHERE sen_no = '016568' OR sen_no = '012250'
    
    UNION ALL
    
    SELECT idn, sen_no, tarix, kontra, NULL as sifaris
    FROM sm_sif_sened WITH (NOLOCK)
    WHERE sen_no = '016568' OR sen_no = '012250'
"""
res = query(sql)
print("Orders by sen_no 016568 and 012250:")
for r in res:
    print(r)
