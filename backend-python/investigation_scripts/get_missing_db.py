import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.erp_connector import query

sql = """
SELECT [Sifariscesidi], [Tarix], [Musteri], [Senednomresi], [Status]
FROM [sa].[Sifarishesabat_2]
WHERE UPPER([Sifariscesidi]) LIKE '%XURMAYI%' OR UPPER([Sifariscesidi]) LIKE '%AYAQ%' OR UPPER([Sifariscesidi]) LIKE '%50X90%'
"""
try:
    rows = query(sql)
    print('Sifarishesabat_2 count:', len(rows))
    for row in rows[:10]:
        print(row)
except Exception as e:
    print(e)
    
sql2 = """
SELECT [Cesid], [Tarix], [Musteri], [Sifaris_No], [Sifarisin_statusu]
FROM [sa].[Sifarisler]
WHERE UPPER([Cesid]) LIKE '%XURMAYI%' OR UPPER([Cesid]) LIKE '%AYAQ%' OR UPPER([Cesid]) LIKE '%50X90%'
"""
try:
    rows = query(sql2)
    print('Sifarisler count:', len(rows))
    for row in rows[:10]:
        print(row)
except Exception as e:
    print(e)
