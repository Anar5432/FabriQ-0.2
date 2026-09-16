import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def find_missing():
    # Find orders (sif_sen) that are missing from sm_rasenka
    # Let's check how many orders exist and how many have rasenka
    
    # First, how many total orders?
    res = query("SELECT COUNT(*) as c FROM sm_sifaris")
    print("Total sm_sifaris:", res[0]['c'])
    
    res2 = query("SELECT COUNT(DISTINCT sif_sen) as c FROM sm_rasenka")
    print("Total sm_rasenka distinct orders:", res2[0]['c'])
    
    # Let's get recent orders missing rasenka (join with sm_sifaris to get details)
    # Since there might be thousands, let's just get the last 20
    q = """
    SELECT TOP 20 s.idn, s.sen_no, s.tarix, s.serh, c.name as customer
    FROM sm_sifaris s
    LEFT JOIN sm_rasenka r ON s.sen_no = r.sif_sen
    LEFT JOIN sm_companies c ON s.ins_user = c.id -- just guessing customer join, let's not join companies if not sure
    WHERE r.sif_sen IS NULL
    ORDER BY s.tarix DESC
    """
    
    q_safe = """
    SELECT TOP 10 s.idn, s.sen_no, s.tarix, s.serh
    FROM sm_sifaris s
    LEFT JOIN sm_rasenka r ON s.sen_no = r.sif_sen
    WHERE r.sif_sen IS NULL
    ORDER BY s.tarix DESC, s.idn DESC
    """
    
    missing = query(q_safe)
    print("\nRecent 10 Orders Missing Rasenka:")
    for m in missing:
        print(f"Order IDN: {m['idn']} | Sen_No: {m['sen_no']} | Tarix: {m['tarix']} | Serh: {m['serh']}")

if __name__ == '__main__':
    find_missing()
