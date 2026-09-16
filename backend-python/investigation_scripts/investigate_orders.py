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
    cursor.execute('''
        SELECT TOP 10 
            t.el_sif, MAX(t.tarix)
        FROM sm_sob_trans t WITH(NOLOCK)
        JOIN sm_sob_trans_el tel WITH(NOLOCK) ON t.idn = tel.es_no
        JOIN sm_goods g WITH(NOLOCK) ON tel.mal = g.idn
        WHERE g.class IN (18, 20) AND t.el_sif IS NOT NULL
        GROUP BY t.el_sif
        ORDER BY MAX(t.tarix) DESC
    ''')
    print("Latest underwear order IDs:", cursor.fetchall())
except Exception as e:
    print(e)
