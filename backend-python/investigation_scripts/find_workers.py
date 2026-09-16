import os, sys, json
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.queries import query

sql = """
WITH RawTasks AS (
    SELECT 
        el_el.emp,
        el_el.miqdar,
        el_el.qiymet,
        el_el.mebleg,
        r_direct.tarix as direct_tarix,
        (SELECT TOP 1 g.name FROM sm_rasenka_mal mal JOIN sm_goods g ON mal.mal = g.idn WHERE mal.es_no = el_el.es_no) as direct_product,
        r_indirect.tarix as indirect_tarix,
        g_indirect.name as indirect_product
    FROM sm_rasenka_el_el el_el (NOLOCK)
    LEFT JOIN sm_rasenka r_direct (NOLOCK) ON el_el.es_no = r_direct.idn
    LEFT JOIN sm_rasenka_mal m_indirect (NOLOCK) ON el_el.es_no = m_indirect.idn
    LEFT JOIN sm_rasenka r_indirect (NOLOCK) ON m_indirect.es_no = r_indirect.idn
    LEFT JOIN sm_goods g_indirect (NOLOCK) ON m_indirect.mal = g_indirect.idn
),
ResolvedTasks AS (
    SELECT 
        emp,
        miqdar,
        qiymet,
        mebleg,
        CASE 
            WHEN direct_tarix IS NOT NULL AND indirect_tarix IS NOT NULL THEN 
                CASE WHEN direct_tarix >= indirect_tarix THEN direct_tarix ELSE indirect_tarix END
            WHEN direct_tarix IS NOT NULL THEN direct_tarix
            ELSE indirect_tarix
        END as resolved_tarix,
        CASE 
            WHEN direct_tarix IS NOT NULL AND indirect_tarix IS NOT NULL THEN 
                CASE WHEN direct_tarix >= indirect_tarix THEN direct_product ELSE indirect_product END
            WHEN direct_tarix IS NOT NULL THEN direct_product
            ELSE indirect_product
        END as product_name
    FROM RawTasks
),
RankedTasks AS (
    SELECT 
        emp,
        CONVERT(VARCHAR(10), resolved_tarix, 120) as tarix,
        product_name,
        miqdar,
        qiymet,
        mebleg,
        ROW_NUMBER() OVER(PARTITION BY emp ORDER BY resolved_tarix DESC) as rn
    FROM ResolvedTasks
    WHERE resolved_tarix IS NOT NULL
)
SELECT * FROM RankedTasks WHERE rn <= 5 AND emp IN (401, 7937, 7956)
"""
res = query(sql)

with open('workers_out.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2, default=str)
