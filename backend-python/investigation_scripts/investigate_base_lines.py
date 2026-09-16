import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
import pyodbc
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
django.setup()

from dashboard.queries import get_dynamic_ym_ids

conn_str = f"DRIVER={{{settings.MSSQL_CONFIG['DRIVER']}}};SERVER={settings.MSSQL_CONFIG['SERVER']};DATABASE=BTFERPDB;UID={settings.MSSQL_CONFIG['USERNAME']};PWD={settings.MSSQL_CONFIG['PASSWORD']};TrustServerCertificate=yes;Encrypt=no;"
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

ym_ids_str = get_dynamic_ym_ids('underwear')
keyword_cond = "(g.name LIKE '%BOXER%' OR g.name LIKE '%KÜLOT%' OR g.name LIKE '%KULOT%' OR g.name LIKE '%MAYKA%' OR g.name LIKE '%BODY%' OR g.name LIKE '%SLİP%' OR g.name LIKE '%SLIP%')"
keyword_prefix = "(g.name LIKE 'HM-%' OR g.name LIKE 'YM-%' OR g.name LIKE 'TM-%')"
cls_cond = f"(g.class = 20 OR ({keyword_cond} AND {keyword_prefix}) OR g.idn IN ({ym_ids_str}))"

date_filter_sened = "AND s.tarix >= DATEADD(YEAR, -2, GETDATE())"

sql = f"""
    SELECT
        s.idn AS order_id,
        s.sen_no,
        s.yekun AS order_total,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
        s.kontra AS company_id,
        c.name AS company_name,
        e.idn AS line_id,
        e.num AS line_num,
        g.idn AS product_id,
        g.name AS product_name,
        e.miqdar AS qty_ordered,
        (e.miqdar - ISNULL(e.sat_miq, 0)) AS qty_remaining,
        NULL AS parent_order_id
    FROM sm_sif_sened s WITH (NOLOCK)
    JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE {cls_cond}
      AND s.idn NOT IN (SELECT sifaris FROM sm_sifaris_form WHERE sifaris IS NOT NULL)
      {date_filter_sened}
      AND s.idn = 4108
"""

try:
    cursor.execute(sql)
    for r in cursor.fetchall():
        print(f"4108 from sm_sif_sened: date={r.tarix}, product={r.product_name}, company_id={r.company_id}, c.name={r.company_name}")
except Exception as e: print(e)
