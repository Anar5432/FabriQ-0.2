import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT 'sm_sifaris_form' as tbl, idn, sen_no, kontra, sifaris FROM sm_sifaris_form WITH (NOLOCK) WHERE kontra IN (840, 905)
    UNION ALL
    SELECT 'sm_sif_sened' as tbl, idn, sen_no, kontra, NULL as sifaris FROM sm_sif_sened WITH (NOLOCK) WHERE kontra IN (840, 905)
"""
res = query(sql)
print("Rows with kontra 840 or 905:")
for r in res:
    print(r)
