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

order_id = 4108

# Check sm_kontr_sat
try:
    cursor.execute(f"SELECT TOP 1 * FROM sm_kontr_sat WHERE idn = {order_id}")
    if cursor.fetchone(): print(f"Found in sm_kontr_sat")
except Exception as e: print("sm_kontr_sat error:", e)

# Check sm_sifaris
try:
    cursor.execute(f"SELECT TOP 1 * FROM sm_sifaris WHERE idn = {order_id}")
    if cursor.fetchone(): print(f"Found in sm_sifaris")
except Exception as e: print("sm_sifaris error:", e)

# Check sm_ist_tap
try:
    cursor.execute(f"SELECT TOP 1 * FROM sm_ist_tap WHERE idn = {order_id}")
    if cursor.fetchone(): print(f"Found in sm_ist_tap")
except Exception as e: print("sm_ist_tap error:", e)
    
# Let's see what tables have a column named el_sif or sif_no
try:
    cursor.execute("SELECT c.name, t.name FROM sys.columns c JOIN sys.tables t ON c.object_id = t.object_id WHERE c.name = 'el_sif' OR c.name = 'sif_no' OR c.name = 'sif_idn'")
    res = cursor.fetchall()
    print("Tables with order ID columns:", set([r[1] for r in res]))
except Exception as e: print(e)
