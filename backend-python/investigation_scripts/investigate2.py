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
    cursor.execute("SELECT c.name FROM sys.columns c JOIN sys.tables t ON c.object_id = t.object_id WHERE t.name = 'sm_goods'")
    cols = [r.name for r in cursor.fetchall()]
    print("sm_goods columns:", cols)

    # Let's find distinct groups or sectors
    if 'sector' in cols:
        cursor.execute("SELECT DISTINCT sector FROM sm_goods")
        print("Sectors:", [r.sector for r in cursor.fetchall()])
    if 'qrup' in cols:
        cursor.execute("SELECT DISTINCT qrup FROM sm_goods")
        print("Qrups:", [r.qrup for r in cursor.fetchall()])
        
except Exception as e:
    print(e)
