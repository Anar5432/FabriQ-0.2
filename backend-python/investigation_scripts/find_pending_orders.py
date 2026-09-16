import sqlite3
import json
import codecs

conn = sqlite3.connect('factory.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

with codecs.open('pending_orders.txt', 'w', 'utf-8') as f:
    cur.execute("SELECT DISTINCT status FROM orders")
    f.write(f"Statuses: {[r[0] for r in cur.fetchall()]}\n")

    query = """
    SELECT * FROM orders
    WHERE status LIKE '%Gözləyir%' OR status LIKE '%Yeni%' OR status LIKE '%Pending%' OR status LIKE '%Sıraya%' OR stage_index = 0
    ORDER BY created_at DESC
    LIMIT 20
    """
    cur.execute(query)
    orders = [dict(r) for r in cur.fetchall()]
    f.write(f"\nFound {len(orders)} pending orders.\n")
    for o in orders:
        f.write(f"{o['id']} | {o['status']} | {o['stage_index']} | {o['created_at']} | {o['product_type']}\n")
