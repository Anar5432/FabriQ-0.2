import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
            SELECT
                s.idn AS order_id, s.sen_no,
                s.kontra AS company_id, c.name AS company_name
            FROM sm_kontr_sat s WITH (NOLOCK)
            JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            WHERE s.kontra = 1731
"""
res = query(sql)
print(f"sm_kontr_sat for 1731: {[r['company_name'] for r in res][:5]}")

sql2 = """
            SELECT
                s.idn AS order_id, s.sen_no,
                s.kontra AS company_id, c.name AS company_name
            FROM sm_sif_sened s WITH (NOLOCK)
            JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            WHERE s.kontra = 1731
"""
res2 = query(sql2)
print(f"sm_sif_sened for 1731: {[r['company_name'] for r in res2][:5]}")
