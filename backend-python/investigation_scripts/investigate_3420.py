import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

order_id = 3420

print(f"--- Investigating Order {order_id} ---")

sql_form = f"""
    SELECT
        s.idn AS order_id, s.kontra AS company_id, c.name AS company_name
    FROM sm_sifaris_form s WITH (NOLOCK)
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    WHERE s.idn = {order_id}
"""
print("sm_sifaris_form:", query(sql_form))

sql_sened = f"""
    SELECT
        s.idn AS order_id, s.kontra AS company_id, c.name AS company_name
    FROM sm_sif_sened s WITH (NOLOCK)
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    WHERE s.idn = {order_id}
"""
print("sm_sif_sened:", query(sql_sened))

sql_sat = f"""
    SELECT
        s.idn AS order_id, s.kontra AS company_id, c.name AS company_name, s.kontra_name
    FROM sm_kontr_sat s WITH (NOLOCK)
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    WHERE s.idn = {order_id}
"""
print("sm_kontr_sat:", query(sql_sat))

