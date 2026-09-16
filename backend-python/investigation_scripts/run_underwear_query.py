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

query = """
SELECT TOP 15
    t.el_sif AS Order_ID,
    MAX(t.tarix) AS Last_Worked_On,
    MIN(t.tarix) AS Started_On,
    g.name AS Product_Name,
    SUM(tel.miqdar) AS Total_Quantity,
    COUNT(t.idn) AS Movement_Count
FROM sm_sob_trans t WITH(NOLOCK)
JOIN sm_sob_trans_el tel WITH(NOLOCK) ON t.idn = tel.es_no
JOIN sm_goods g WITH(NOLOCK) ON tel.mal = g.idn
WHERE 
    t.el_sif IS NOT NULL 
    AND t.el_sif > 0 
    AND t.tesdiq = 1
    AND g.class IN (18, 20)
GROUP BY 
    t.el_sif,
    g.name
ORDER BY 
    MAX(t.tarix) DESC,
    t.el_sif DESC;
"""

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    for r in rows:
        print(f"{r.Order_ID} | {r.Last_Worked_On.strftime('%Y-%m-%d')} | {r.Started_On.strftime('%Y-%m-%d')} | {r.Product_Name} | {r.Total_Quantity} | {r.Movement_Count}")
except Exception as e:
    print(e)
