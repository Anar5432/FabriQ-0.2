import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
WITH MisclassifiedProducts AS (
    SELECT idn 
    FROM sm_goods 
    WHERE (name LIKE '%BOXER%' 
        OR name LIKE '%MAYKA%' 
        OR name LIKE '%KÜLOT%' 
        OR name LIKE '%BODY%' 
        OR name LIKE '%SLİP%')
      AND (class != 20 OR class IS NULL)
)
SELECT 
    'sm_sifaris_form' as source,
    s.idn AS order_id,
    s.sen_no,
    c.name as company_name,
    s.tarix
FROM sm_sifaris_form s WITH (NOLOCK)
JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
WHERE e.mal IN (SELECT idn FROM MisclassifiedProducts)
  AND (s.sen_no IS NULL OR LTRIM(RTRIM(s.sen_no)) = '')

UNION ALL

SELECT 
    'sm_sif_sened' as source,
    s.idn AS order_id,
    s.sen_no,
    c.name as company_name,
    s.tarix
FROM sm_sif_sened s WITH (NOLOCK)
JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
WHERE e.mal IN (SELECT idn FROM MisclassifiedProducts)
  AND (s.sen_no IS NULL OR LTRIM(RTRIM(s.sen_no)) = '')
"""
try:
    res = query(sql)
    print(f"Total rows found missing sen_no for excluded underwear products: {len(res)}")
    seen = set()
    dedup = []
    for r in res:
        if r['order_id'] not in seen:
            seen.add(r['order_id'])
            dedup.append(r)
    
    for r in dedup:
        print(r)
except Exception as e:
    print(e)
