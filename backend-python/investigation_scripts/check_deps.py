import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT idn, name FROM sm_depo")
    print("--- Depolar ---")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")
except Exception as e:
    print(e)
    
try:
    cursor.execute("SELECT idn, name FROM sm_ist_sexi")
    print("\n--- Istehsal Sexleri ---")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")
except Exception as e:
    print(e)

conn.close()
