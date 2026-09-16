import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
import pyodbc
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
django.setup()

conn_str = f"DRIVER={{{settings.MSSQL_CONFIG['DRIVER']}}};SERVER={settings.MSSQL_CONFIG['SERVER']};DATABASE=BTFERPDB;UID={settings.MSSQL_CONFIG['USERNAME']};PWD={settings.MSSQL_CONFIG['PASSWORD']};TrustServerCertificate=yes;Encrypt=no;"
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

print("--- Tables starting with sm_process ---")
cursor.execute("SELECT name FROM sys.tables WHERE name LIKE 'sm_process%'")
for row in cursor.fetchall():
    print(row.name)

print("\n--- Try finding categories in sm_goods ---")
try:
    cursor.execute("SELECT TOP 5 column_name FROM information_schema.columns WHERE table_name = 'sm_goods'")
    for row in cursor.fetchall():
        print(row.column_name)
except Exception as e:
    print(e)
