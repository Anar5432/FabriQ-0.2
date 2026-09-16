import os
import django
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def fetch_data():
    try:
        # Check how sm_process_iz connects to orders
        cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_process_iz'")
        print("sm_process_iz cols:", [c['COLUMN_NAME'] for c in cols])
        
        # Look for a few recent orders and their process records
        proc = query("SELECT TOP 5 * FROM sm_process_iz ORDER BY idn DESC")
        for p in proc:
            print("Process record:", p)
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fetch_data()
