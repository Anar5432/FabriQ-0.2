import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query
from datetime import datetime

print("--- ANALYZING COMPLETED ORDERS VS MUDDET ---")

sql = """
SELECT TOP 20
    s.idn AS order_id,
    s.sen_no AS order_no,
    s.tarix AS order_date,
    hm_goods.idn AS hm_mal,
    hm_goods.name AS product_name,
    hm_goods.muddet AS db_muddet,
    e.miqdar AS qty_ordered
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods hm_goods WITH (NOLOCK) ON e.mal = hm_goods.idn
WHERE hm_goods.class = 27
  AND e.qaliq = 0
  AND hm_goods.muddet > 0
ORDER BY s.tarix DESC
"""
orders = query(sql)

results = []

for o in orders:
    # Find the earliest cutting transfer AFTER the order date (Production Start)
    # and the latest warehouse transfer AFTER the order date (Production End)
    # Using YM- logic
    sql_trans = f"""
    SELECT 
        MIN(t.tarix) AS start_date,
        MAX(t.tarix) AS end_date
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    JOIN sm_goods ym_g WITH (NOLOCK) ON tel.mal = ym_g.idn
    WHERE t.tesdiq = 1 
      AND (
          ym_g.idn = {o['hm_mal']}
          OR (ym_g.name LIKE 'YM-%' AND '{o['product_name']}' LIKE 'HM-%'
              AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING('{o['product_name']}', 4, LEN('{o['product_name']}')))
      )
      AND t.tarix >= '{o['order_date']}'
    """
    trans = query(sql_trans)
    
    start_date = trans[0]['start_date'] if trans else None
    end_date = trans[0]['end_date'] if trans else None
    
    if start_date and end_date and start_date != end_date:
        delta = end_date - start_date
        days = delta.days
        if days > 0:
            qty = float(o['qty_ordered'])
            db_muddet = float(o['db_muddet'])
            
            # Empirical time per piece in days and minutes
            days_per_piece = days / qty
            minutes_per_piece = days_per_piece * 24 * 60
            
            results.append({
                'order': o['order_no'],
                'product': o['product_name'],
                'qty': qty,
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'days_total': days,
                'minutes_per_piece': round(minutes_per_piece, 2),
                'db_muddet': db_muddet
            })

print(f"Found {len(results)} valid Make-to-Order examples with muddet data.")
for r in results[:5]:
    print(r)
    
