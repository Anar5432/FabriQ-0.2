import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
    SELECT TOP 5 idn, sif_no FROM sm_good_ist WHERE sif_no IN (20304, 3553)
"""
try:
    print("sm_good_ist (sif_no):")
    print(query(sql))
except Exception as e:
    print(e)
    
sql2 = """
    SELECT TOP 5 idn, el_sif FROM sm_sob_trans WHERE el_sif IN (20304, 3553)
"""
try:
    print("\nsm_sob_trans (el_sif):")
    print(query(sql2))
except Exception as e:
    print(e)
