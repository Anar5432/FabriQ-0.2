import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    sql_pending = f\"\"\"
    SET NOCOUNT ON;
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
        e.qaliq AS qty_remaining,
        0 AS current_phase,
        '' AS phase_name
    FROM sm_sifaris_form s WITH (NOLOCK)
    JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
    LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE g.class IN (11, 28)
      AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    ORDER BY c.name, s.tarix DESC, e.num;
    \"\"\"
    print("Running query...")
    rows = query(sql_pending)
    print(f"Got {len(rows)} rows.")
    for r in rows[:10]:
        print(r)

if __name__ == '__main__':
    check_logic()
