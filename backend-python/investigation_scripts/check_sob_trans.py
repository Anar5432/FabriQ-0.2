import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sob_trans'")
    cols = cursor.fetchall()
    print("--- sm_sob_trans ---")
    for c in cols:
        print(f"  {c[0]} ({c[1]})")
        
    cursor.execute("SELECT TOP 5 is_ad, sob, emel_nov FROM sm_sob_trans WHERE is_ad IS NOT NULL OR emel_nov IS NOT NULL")
    print(cursor.fetchall())
except Exception as e:
    print(e)

conn.close()
