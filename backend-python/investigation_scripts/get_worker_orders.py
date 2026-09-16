import pymssql
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = pymssql.connect(
    server='192.168.100.1:1433',
    user='User1',
    password='bfzY7835WCS72M',
    database='BTFERPDB',
    charset='UTF-8',
    autocommit=True
)

cursor = conn.cursor(as_dict=True)

cursor.execute(SELECT idn, name FROM sm_good_class)
classes = cursor.fetchall()

sql_prod = "
SELECT TOP 40
    s.idn AS order_id,
    s.sen_no,
    CONVERT(VARCHAR(10), s.tarix, 23) AS order_date,
    ISNULL(c.name, s.kontra_name) AS customer_name,
    g.idn AS product_id,
    g.name AS product_name,
    cl.name AS class_name,
    g.class AS class_id,
    e.miqdar AS qty,
    s.yekun AS order_total,
    'sm_sifaris_form' AS src
FROM sm_sifaris_form s WITH (NOLOCK)
JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN sm_good_class cl WITH (NOLOCK) ON g.class = cl.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
WHERE (
    g.class IN (22, 24, 27, 31, 32, 34)
    OR (g.name LIKE 'HM-%' AND (g.name LIKE '%KOMBIN%' OR g.name LIKE '%KOST%' OR g.name LIKE '%SALOP%' OR g.name LIKE '%XALAT%' OR g.name LIKE '%JİLET%'))
)
ORDER BY s.tarix DESC, s.idn DESC
"
cursor.execute(sql_prod)
prod_orders = cursor.fetchall()

sql_sales = "
SELECT TOP 40
    s.idn AS order_id,
    s.sen_no,
    CONVERT(VARCHAR(10), s.tarix, 23) AS order_date,
    ISNULL(COALESCE(c.name, s.kontra_name), 'Bilinməyən') AS customer_name,
    g.idn AS product_id,
    g.name AS product_name,
    cl.name AS class_name,
    g.class AS class_id,
    e.miqdar AS qty,
    s.yekun AS order_total,
    'sm_sif_sened' AS src
FROM sm_sif_sened s WITH (NOLOCK)
JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
LEFT JOIN sm_good_class cl WITH (NOLOCK) ON g.class = cl.idn
LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
WHERE (
    g.class IN (22, 24, 27, 31, 32, 34)
    OR (g.name LIKE 'HM-%' AND (g.name LIKE '%KOMBIN%' OR g.name LIKE '%KOST%' OR g.name LIKE '%SALOP%' OR g.name LIKE '%XALAT%' OR g.name LIKE '%JİLET%'))
)
AND NOT EXISTS (SELECT 1 FROM sm_sifaris_form sf WITH (NOLOCK) WHERE sf.sifaris = s.idn)
ORDER BY s.tarix DESC, s.idn DESC
"
cursor.execute(sql_sales)
sales_orders = cursor.fetchall()

conn.close()

with open('latest_worker_orders.json', 'w', encoding='utf-8') as f:
    json.dump({
        'classes': classes,
        'prod_orders': prod_orders,
        'sales_orders': sales_orders
    }, f, ensure_ascii=False, indent=2, default=str)

print(fDONE: prod={len(prod_orders)}, sales={len(sales_orders)})
