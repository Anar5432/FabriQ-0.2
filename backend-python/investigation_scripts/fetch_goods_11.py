import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT name FROM sm_goods WHERE idn = 11")
    print("Goods 11:", cursor.fetchone())
except Exception as e:
    print(e)
    
try:
    cursor.execute("SELECT * FROM sm_process_iz TOP 1")
    print(cursor.fetchone())
except:
    pass

conn.close()
