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
    cursor.execute("SELECT TOP 5 emp1, emp2, ins_user FROM sm_sob_trans WHERE sobe2 IN (3, 24)")
    print("sm_sob_trans emps:", cursor.fetchall())
except Exception as e:
    print(e)
    
try:
    cursor.execute("SELECT name FROM sys.tables WHERE name LIKE '%kadr%' OR name LIKE '%emp%' OR name LIKE '%isci%' OR name LIKE '%user%'")
    print("Employee tables:", [r.name for r in cursor.fetchall()])
except Exception as e:
    print(e)
    
try:
    cursor.execute("SELECT c.name FROM sys.columns c JOIN sys.tables t ON c.object_id = t.object_id WHERE t.name = 'sm_sobeler_med'")
    print("sm_sobeler_med cols:", [r.name for r in cursor.fetchall()])
except Exception as e:
    print(e)
