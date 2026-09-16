import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import get_orders, query, get_sector_rules

sector = 'underwear'
rules = get_sector_rules(sector)
cls_cond = rules['class_condition']
date_filter_form = ""
date_filter_sened = ""

sql = f"""
    SET NOCOUNT ON;
      
    SELECT
        ISNULL(s.sifaris, s.idn) AS order_id,
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
        e.miqdar AS qty_remaining,
        NULL AS parent_order_id
    FROM sm_sifaris_form s WITH (NOLOCK)
    JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE {cls_cond}
      {date_filter_form}
      
    UNION ALL
    
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
      
    ORDER BY tarix ASC, line_num;
"""
base_lines = query(sql, cache_key=None)

# Find any 3420 in base_lines
for idx, row in enumerate(base_lines):
    if row['order_id'] == 3420:
        if row['company_id'] is None or row['company_name'] is None or row['company_name'] == 'Bilinməyən':
            print(f"FOUND BAD ROW: {row}")
            
# Also check missing_lines for 3420!
sql_missing = f"""
            SET NOCOUNT ON;
            SELECT
                s.idn AS order_id, s.sen_no, s.tam_yek AS order_total,
                CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
                s.kontra AS company_id, c.name AS company_name,
                e.idn AS line_id, e.num AS line_num, g.idn AS product_id,
                g.name AS product_name, e.miqdar AS qty_ordered, 0 AS qty_remaining,
                NULL AS parent_order_id
            FROM sm_kontr_sat s WITH (NOLOCK)
            JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
            WHERE s.idn = 3420
            UNION ALL
            SELECT
                s.idn AS order_id, s.sen_no, s.yekun AS order_total,
                CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
                s.kontra AS company_id, c.name AS company_name,
                e.idn AS line_id, e.num AS line_num, g.idn AS product_id,
                g.name AS product_name, e.miqdar AS qty_ordered, e.miqdar AS qty_remaining,
                s.sifaris AS parent_order_id
            FROM sm_sifaris_form s WITH (NOLOCK)
            JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
            LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
            JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
            WHERE s.idn = 3420
            """
missing_lines = query(sql_missing, cache_key=None)
for row in missing_lines:
    print(f"MISSING LINE 3420: {row}")

