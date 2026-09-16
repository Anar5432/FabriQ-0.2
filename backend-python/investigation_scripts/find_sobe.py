import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT idn, name FROM sm_sex")
    cols = cursor.fetchall()
    print("--- Sex (Departments) ---")
    for c in cols:
        print(f"{c[0]}: {c[1]}")
except Exception as e:
    print(e)

conn.close()
