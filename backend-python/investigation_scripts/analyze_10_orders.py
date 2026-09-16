import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

print("--- ANALYZING 10 SPECIFIC CORPORATE WEAR ORDERS ---")

sql = """
SELECT TOP 30
    s.idn AS order_id,
    s.sen_no AS order_no,
    s.kontra_name as customer,
    CONVERT(VARCHAR(10), s.tarix, 23) AS order_date,
    hm_goods.idn AS hm_mal,
    hm_goods.name AS product_name,
    hm_goods.muddet AS db_muddet,
    e.miqdar AS qty_ordered
FROM sm_kontr_sat s WITH (NOLOCK)
JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods hm_goods WITH (NOLOCK) ON e.mal = hm_goods.idn
WHERE hm_goods.class = 27
  AND hm_goods.muddet > 0
  AND e.miqdar >= 10  -- Filter out tiny orders
ORDER BY s.tarix DESC
"""
orders = query(sql)

results = []
seen_products = set()

for o in orders:
    if len(results) >= 10:
        break
    
    # Optional: ensure we look at distinct products or orders for variety
    if o['product_name'] in seen_products:
        continue

    sql_trans = f"""
    SELECT 
        MIN(t.tarix) AS start_date,
        MAX(t.tarix) AS end_date,
        SUM(CASE WHEN t.sobe2 = 6 THEN tel.miqdar ELSE 0 END) as total_produced
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    JOIN sm_goods ym_g WITH (NOLOCK) ON tel.mal = ym_g.idn
    WHERE t.tesdiq = 1 
      AND (
          ym_g.idn = {o['hm_mal']}
          OR (ym_g.name LIKE 'YM-%' AND '{o['product_name']}' LIKE 'HM-%'
              AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING('{o['product_name']}', 4, LEN('{o['product_name']}')))
      )
      -- Look at production window up to 90 days before and 30 days after the order
      AND t.tarix >= DATEADD(DAY, -90, '{o['order_date']}')
      AND t.tarix <= DATEADD(DAY, 30, '{o['order_date']}')
    """
    trans = query(sql_trans)
    
    start_date = trans[0]['start_date'] if trans else None
    end_date = trans[0]['end_date'] if trans else None
    produced = float(trans[0]['total_produced'] or 0)
    
    if start_date and end_date and start_date != end_date and produced > 0:
        delta = end_date - start_date
        days = delta.days
        if days >= 0:
            # If days is 0 (same day), let's assume it took at least 8 hours (1 working day) to avoid div by zero
            calc_days = max(1, days)
            db_muddet = float(o['db_muddet'])
            
            # Empirical time per piece based on the batch produced around this order
            days_per_piece = calc_days / produced
            minutes_per_piece = days_per_piece * 24 * 60
            
            results.append({
                'customer': o['customer'],
                'order': o['order_no'],
                'order_date': o['order_date'],
                'product': o['product_name'],
                'qty_ordered': float(o['qty_ordered']),
                'qty_produced_batch': produced,
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'days_total': calc_days,
                'minutes_per_piece': round(minutes_per_piece, 2),
                'db_muddet': db_muddet
            })
            seen_products.add(o['product_name'])

for r in results:
    print(r)
