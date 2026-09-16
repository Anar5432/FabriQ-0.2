import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
import pyodbc
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
django.setup()

conn_str = f"DRIVER={{{settings.MSSQL_CONFIG['DRIVER']}}};SERVER={settings.MSSQL_CONFIG['SERVER']};DATABASE=BTFERPDB;UID={settings.MSSQL_CONFIG['USERNAME']};PWD={settings.MSSQL_CONFIG['PASSWORD']};TrustServerCertificate=yes;Encrypt=no;"
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

try:
    sql = """
            SELECT
                s.idn AS order_id, s.kontra AS company_id, c.name AS company_name, s.kontra_name AS old_company_name
            FROM sm_kontr_sat s WITH (NOLOCK)
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            WHERE s.idn = 4108
    """
    cursor.execute(sql)
    for r in cursor.fetchall():
        print(f"4108 from sm_kontr_sat: company_id={r.company_id}, c.name={r.company_name}, s.kontra_name={r.old_company_name}")
        
    sql_form = """
            SELECT
                s.idn AS order_id, s.kontra AS company_id, c.name AS company_name
            FROM sm_sifaris_form s WITH (NOLOCK)
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            WHERE s.idn = 4108
    """
    cursor.execute(sql_form)
    for r in cursor.fetchall():
        print(f"4108 from sm_sifaris_form: company_id={r.company_id}, c.name={r.company_name}")

    sql_sened = """
            SELECT
                s.idn AS order_id, s.kontra AS company_id, c.name AS company_name
            FROM sm_sif_sened s WITH (NOLOCK)
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            WHERE s.idn = 4108
    """
    cursor.execute(sql_sened)
    for r in cursor.fetchall():
        print(f"4108 from sm_sif_sened: company_id={r.company_id}, c.name={r.company_name}")
        
except Exception as e: print(e)
