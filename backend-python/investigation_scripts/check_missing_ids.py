import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
WITH SourceData AS (
    SELECT
        ISNULL(s.sifaris, s.idn) AS order_id,
        s.sen_no,
        s.yekun AS order_total,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
        s.kontra AS company_id,
        c.name AS company_name,
        1 as Sector
    FROM sm_sifaris_form s
    LEFT JOIN sm_kontra c ON s.kontra = c.idn
    WHERE s.r = 0

    UNION ALL

    SELECT
        ISNULL(s.sifaris, s.idn) AS order_id,
        s.sen_no,
        s.yekun AS order_total,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
        s.kontra AS company_id,
        c.name AS company_name,
        1 as Sector
    FROM sm_sif_sened s
    LEFT JOIN sm_kontra c ON s.kontra = c.idn
    WHERE s.nov IS NULL
      AND s.r = 0
      AND s.idn NOT IN (SELECT sifaris FROM sm_sifaris_form WHERE sifaris IS NOT NULL)
)
SELECT * FROM SourceData
WHERE order_id IS NULL OR sen_no IS NULL OR LTRIM(RTRIM(sen_no)) = '' OR order_id = 0
"""
try:
    res = query(sql)
    print(f"Found {len(res)} orders missing order_id or sen_no in Underwear.")
    for r in res[:10]:
        print(r)
except Exception as e:
    print(e)
