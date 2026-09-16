import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()
from django.conf import settings
import pymssql

server = settings.MSSQL_CONFIG['SERVER'].replace(',', ':')
conn = pymssql.connect(
    server=server,
    user=settings.MSSQL_CONFIG['USERNAME'],
    password=settings.MSSQL_CONFIG['PASSWORD'],
    database=settings.MSSQL_CONFIG['DATABASE'],
    charset='cp1254',
    autocommit=True
)
cursor = conn.cursor()
cursor.execute("SELECT c.name FROM sm_kontra c WHERE idn = 1731")
print(f"pymssql CP1254 output: {cursor.fetchone()}")

conn2 = pymssql.connect(
    server=server,
    user=settings.MSSQL_CONFIG['USERNAME'],
    password=settings.MSSQL_CONFIG['PASSWORD'],
    database=settings.MSSQL_CONFIG['DATABASE'],
    autocommit=True
)
cursor2 = conn2.cursor()
cursor2.execute("SELECT c.name FROM sm_kontra c WHERE idn = 1731")
print(f"pymssql NO CHARSET output: {cursor2.fetchone()}")

import pyodbc
conn_str = f"DRIVER={{{settings.MSSQL_CONFIG['DRIVER']}}};SERVER={settings.MSSQL_CONFIG['SERVER']};DATABASE={settings.MSSQL_CONFIG['DATABASE']};UID={settings.MSSQL_CONFIG['USERNAME']};PWD={settings.MSSQL_CONFIG['PASSWORD']};TrustServerCertificate=yes;Encrypt=no;"
conn3 = pyodbc.connect(conn_str, autocommit=True)
cursor3 = conn3.cursor()
cursor3.execute("SELECT c.name FROM sm_kontra c WHERE idn = 1731")
print(f"pyodbc output: {cursor3.fetchone()}")
