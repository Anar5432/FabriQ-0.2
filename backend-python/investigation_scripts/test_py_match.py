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
    
    start_fetch = time.time()
    sql = "SELECT idn, name, class FROM sm_goods WITH (NOLOCK)"
    rows = query(sql)
    end_fetch = time.time()
    
    start_proc = time.time()
    target_classes = {22, 24, 27, 31, 32, 34}
    
    hm_prefixes = set()
    for r in rows:
        cls = r['class']
        name = r['name'] or ''
        if cls in target_classes and name.startswith('HM-'):
            prefix = name.split(' ')[0]
            hm_prefixes.add(prefix)
            
    matched_ids = []
    for r in rows:
        if r['class'] is None:
            name = r['name'] or ''
            if name.startswith('YM-'):
                hm_equiv = name.split(' ')[0].replace('YM-', 'HM-', 1)
                if hm_equiv in hm_prefixes:
                    matched_ids.append(str(r['idn']))
            elif name.startswith('TM-'):
                hm_equiv = name.split(' ')[0].replace('TM-', 'HM-', 1)
                if hm_equiv in hm_prefixes:
                    matched_ids.append(str(r['idn']))
    end_proc = time.time()
    
    out.write(f"Fetch time: {end_fetch - start_fetch:.3f} seconds\n")
    out.write(f"Process time: {end_proc - start_proc:.3f} seconds\n")
    out.write(f"Matched YM/TM IDs: {len(matched_ids)}\n")
            
    with io.open("test_py_match.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    test()
