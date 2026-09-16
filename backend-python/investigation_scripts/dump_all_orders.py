import sqlite3
import codecs

conn = sqlite3.connect('factory.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

query = "SELECT * FROM orders"
cur.execute(query)
orders = cur.fetchall()

with codecs.open('all_orders.txt', 'w', 'utf-8') as f:
    for o in orders:
        f.write(f"{dict(o)}\n")
