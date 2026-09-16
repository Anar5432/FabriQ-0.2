# -*- coding: utf-8 -*-
import os
import django
import io
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    cls = '(22, 24, 27, 31, 32, 34)'
    
    start_cache = time.time()
    # Cache query
    sql_ids = f"""
    SELECT g.idn
    FROM sm_goods g WITH (NOLOCK)
    WHERE g.class IS NULL AND g.name LIKE 'YM-%'
      AND EXISTS (
          SELECT 1 FROM sm_goods h WITH (NOLOCK)
          WHERE h.name LIKE REPLACE(SUBSTRING(g.name, 1, CHARINDEX(' ', g.name + ' ') - 1), 'YM-', 'HM-') + '%'
            AND h.class IN {cls}
      )
    """
    rows_ids = query(sql_ids)
    ym_ids = [str(r['idn']) for r in rows_ids]
    end_cache = time.time()
    
    ym_ids_str = ",".join(ym_ids) if ym_ids else "0"
    
    q_pending = f"""
        SELECT
            s.idn AS order_id,
            s.sen_no,
            c.name AS company_name,
            e.idn AS line_id,
            g.name AS product_name,
            e.miqdar AS qty_ordered
        FROM sm_sifaris_form s WITH (NOLOCK)
        JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
        LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE (g.class IN {cls} OR g.idn IN ({ym_ids_str}))
          AND s.tarix >= DATEADD(DAY, -60, GETDATE())
    """
    start_q = time.time()
    rows = query(q_pending)
    end_q = time.time()
    
    out.write(f"Cache query taken: {end_cache - start_cache:.2f} seconds\n")
    out.write(f"Found YM IDs: {len(ym_ids)}\n")
    out.write(f"Main query taken: {end_q - start_q:.2f} seconds\n")
    out.write(f"Rows returned: {len(rows)}\n")
            
    with io.open("test_cache.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
