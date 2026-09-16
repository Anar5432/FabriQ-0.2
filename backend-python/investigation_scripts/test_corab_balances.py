# -*- coding: utf-8 -*-
import sys, os, django
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.erp_connector import query

def test_corab():
    # Let's check if sm_sob_trans is used for corab products
    # Check sm_sobeler_med to see if it tracks quantities per faza
    q = """
    SELECT TOP 10 sm.idn, sm.anbar, sm.faza, sm.sif_no, sm.mal, sm.miqdar, g.name
    FROM sm_sobeler_med sm WITH (NOLOCK)
    JOIN sm_goods g WITH (NOLOCK) ON sm.mal = g.idn
    WHERE g.class IN (21, 29, 30) AND sm.tarix >= DATEADD(DAY, -30, GETDATE())
    """
    rows = query(q)
    print(f"\nRecent sm_sobeler_med (Corab): {len(rows)}")
    for r in rows:
        print(f"ID: {r['idn']} | Sif_No: {r['sif_no']} | Mal: {r['mal']} ({r['name']}) | Faza: {r['faza']} | Qty: {r['miqdar']}")

if __name__ == '__main__':
    test_corab()
