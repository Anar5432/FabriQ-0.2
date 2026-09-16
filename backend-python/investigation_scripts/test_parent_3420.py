import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT
        s.idn AS actual_idn, s.sifaris AS parent_id, s.sen_no, s.kontra
    FROM sm_sifaris_form s WITH (NOLOCK)
    WHERE s.sifaris = 3420 OR s.sen_no = '019472'
"""
res = query(sql)
print("sm_sifaris_form with parent=3420 or sen_no=019472:")
for r in res:
    print(r)
