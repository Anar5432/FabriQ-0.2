import sys, os
from datetime import datetime, timedelta
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

print("=== TABLE 1: ORDER 3299 WITH TRANSFER DETAILS ===")
q1 = """
SELECT TOP 15
    t.el_sif AS Order_ID,
    MAX(t.tarix) AS Last_Worked_On,
    g.name AS Product_Name,
    SourceModule.name AS From_Stage,
    DestModule.name AS To_Stage,
    SUM(tel.miqdar) AS Total_Quantity
FROM sm_sob_trans t WITH(NOLOCK)
JOIN sm_sob_trans_el tel WITH(NOLOCK) ON t.idn = tel.es_no
JOIN sm_goods g WITH(NOLOCK) ON tel.mal = g.idn
LEFT JOIN sm_depo SourceModule WITH(NOLOCK) ON t.sobe1 = SourceModule.idn
LEFT JOIN sm_depo DestModule WITH(NOLOCK) ON t.sobe2 = DestModule.idn
WHERE 
    t.el_sif = 3299
    AND t.tesdiq = 1
    AND g.class IN (18, 20)
GROUP BY 
    t.el_sif,
    g.name,
    SourceModule.name,
    DestModule.name
ORDER BY 
    MAX(t.tarix) DESC, Total_Quantity DESC;
"""
cursor.execute(q1)
for r in cursor.fetchall():
    print(f"{r.Order_ID} | {r.Last_Worked_On.strftime('%Y-%m-%d')} | {r.Product_Name} | {r.From_Stage} | {r.To_Stage} | {r.Total_Quantity}")

print("\n=== TABLE 2: LAST 7 DAYS TRANSFERS ===")
q2 = """
SELECT TOP 20
    t.el_sif AS Order_ID,
    t.tarix AS Transfer_Date,
    g.name AS Product_Name,
    SourceModule.name AS From_Stage,
    DestModule.name AS To_Stage,
    tel.miqdar AS Quantity
FROM sm_sob_trans t WITH(NOLOCK)
JOIN sm_sob_trans_el tel WITH(NOLOCK) ON t.idn = tel.es_no
JOIN sm_goods g WITH(NOLOCK) ON tel.mal = g.idn
LEFT JOIN sm_depo SourceModule WITH(NOLOCK) ON t.sobe1 = SourceModule.idn
LEFT JOIN sm_depo DestModule WITH(NOLOCK) ON t.sobe2 = DestModule.idn
WHERE 
    t.el_sif IS NOT NULL 
    AND t.tesdiq = 1
    AND g.class IN (18, 20)
    AND t.tarix >= DATEADD(day, -7, GETDATE())
ORDER BY 
    t.tarix DESC, t.idn DESC;
"""
cursor.execute(q2)
for r in cursor.fetchall():
    print(f"{r.Order_ID} | {r.Transfer_Date.strftime('%Y-%m-%d')} | {r.Product_Name} | {r.From_Stage} | {r.To_Stage} | {r.Quantity}")
