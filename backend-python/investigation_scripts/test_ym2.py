# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def test():
    out = io.StringIO()
    # Find distinct prefix up to the first space or hyphen, but maybe just check if there are others like YM-
    q1 = """
        SELECT SUBSTRING(name, 1, 3) as pref, COUNT(*) as c
        FROM sm_goods
        WHERE class IS NULL
        GROUP BY SUBSTRING(name, 1, 3)
        ORDER BY c DESC
    """
    rows = query(q1)
    for r in rows:
        out.write(f"Prefix: {r['pref']} | Count: {r['c']}\n")
    with io.open("test_ym2.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
