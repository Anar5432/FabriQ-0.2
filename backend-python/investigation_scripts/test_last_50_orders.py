import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT TOP 50
        s.idn AS Order_ID,
        s.sen_no AS Document_No,
        CONVERT(VARCHAR(10), s.tarix, 23) AS Order_Date,
        ISNULL(c.name, s.kontra_name) AS Customer_Name,
        g.name AS Product_Name,
        e.miqdar AS Quantity,
        s.yekun AS Total_Amount,
        CASE 
            WHEN s.status = 1 THEN 'Tamamlanib'
            WHEN s.status = 2 THEN 'Gozleyir'
            ELSE 'Davam edir' 
        END as Status
    FROM sm_sif_sened s WITH (NOLOCK)
    JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    ORDER BY s.tarix DESC, s.idn DESC
"""
res = query(sql)
print(f"Found {len(res)} rows. First 5 rows:")
for r in res[:5]:
    print(r)
