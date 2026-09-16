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
WITH RankedTransfers AS (
    SELECT 
        t.el_sif AS Order_ID,
        t.tarix AS Transfer_Date,
        g.name AS Product_Name,
        SourceModule.name AS From_Stage,
        DestModule.name AS To_Stage,
        tel.miqdar AS Quantity,
        ROW_NUMBER() OVER(PARTITION BY t.el_sif ORDER BY t.tarix DESC, t.idn DESC) as rn
    FROM sm_sob_trans t WITH(NOLOCK)
    JOIN sm_sob_trans_el tel WITH(NOLOCK) ON t.idn = tel.es_no
    JOIN sm_goods g WITH(NOLOCK) ON tel.mal = g.idn
    LEFT JOIN sm_depo SourceModule WITH(NOLOCK) ON t.sobe1 = SourceModule.idn
    LEFT JOIN sm_depo DestModule WITH(NOLOCK) ON t.sobe2 = DestModule.idn
    WHERE 
        t.el_sif IS NOT NULL 
        AND t.tesdiq = 1
        AND g.class IN (18, 20)
)
SELECT TOP 15
    Order_ID,
    Transfer_Date,
    Product_Name,
    From_Stage,
    To_Stage,
    Quantity
FROM RankedTransfers
WHERE rn = 1 -- Only get the single most recent transfer for each distinct order!
ORDER BY Transfer_Date DESC;
"""
cursor.execute(query)
for r in cursor.fetchall():
    print(f"{r.Order_ID} | {r.Transfer_Date.strftime('%Y-%m-%d')} | {r.Product_Name} | {r.From_Stage} | {r.To_Stage} | {r.Quantity}")
