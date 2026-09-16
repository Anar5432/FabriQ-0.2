import sqlite3
import sys

conn = sqlite3.connect('factory.db')
cur = conn.cursor()

tables = [
    'materials', 'stages', 'orders', 'material_stocks', 
    'product_boms', 'order_material_reserves', 
    'product_processes', 'order_stage_assignments'
]

with open('db_schema_dump.txt', 'w', encoding='utf-8') as f:
    for t in tables:
        f.write(f"\n--- Table: {t} ---\n")
        cur.execute(f"PRAGMA table_info({t});")
        cols = cur.fetchall()
        for c in cols:
            f.write(f"{c}\n")
        
        cur.execute(f"SELECT * FROM {t} LIMIT 1;")
        row = cur.fetchone()
        f.write(f"Sample row: {row}\n")

print("Done.")
