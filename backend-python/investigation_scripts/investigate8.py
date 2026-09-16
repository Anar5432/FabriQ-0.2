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

try:
    cursor.execute("SELECT idn, name FROM sm_faza")
    print("sm_faza:", cursor.fetchall())
except Exception as e:
    print(e)
    
try:
    cursor.execute("SELECT name FROM sys.tables WHERE name LIKE '%anb%' OR name LIKE '%depo%' OR name LIKE '%sob%'")
    print("Potential targets:", [r.name for r in cursor.fetchall()])
except Exception as e:
    print(e)
