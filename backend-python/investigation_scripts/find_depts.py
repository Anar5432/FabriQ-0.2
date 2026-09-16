import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%sex%' OR TABLE_NAME LIKE '%sobe%' OR TABLE_NAME LIKE '%anb%' OR TABLE_NAME LIKE '%dep%' OR TABLE_NAME LIKE '%tikis%' OR TABLE_NAME LIKE '%kesim%'")
    tables = [r[0] for r in cursor.fetchall()]
    print("Matched Tables:")
    print(tables)
except Exception as e:
    print(e)

conn.close()
