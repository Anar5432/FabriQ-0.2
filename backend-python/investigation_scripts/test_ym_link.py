# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    cls = '(22, 24, 27, 31, 32, 34)'
    q = f"""
        SELECT TOP 20 g.idn, g.name, g.class 
        FROM sm_goods g
        WHERE g.class IS NULL
          AND g.name LIKE 'YM-%'
          AND EXISTS (
              SELECT 1 FROM sm_goods h
              WHERE h.class IN {cls}
                AND SUBSTRING(h.name, 1, CHARINDEX(' ', h.name + ' ') - 1) = REPLACE(SUBSTRING(g.name, 1, CHARINDEX(' ', g.name + ' ') - 1), 'YM-', 'HM-')
          )
    """
    rows = query(q)
    if rows:
        for r in rows:
            out.write(f"ID: {r['idn']} | Name: {r['name']} | Class: {r['class']}\n")
    else:
        out.write("No matching YM products found.\n")
        
    with io.open("test_ym_link.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
