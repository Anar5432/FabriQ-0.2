import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()
from dashboard.queries import query

sql = """
SELECT name, class 
FROM sm_goods 
WHERE class IN (22, 24, 27, 31, 32, 34)
  AND (name LIKE 'HM-CAN%' OR name LIKE 'HM-L-Z%')
"""
rows = query(sql)
for r in rows:
    print(r['name'].encode('ascii', 'ignore').decode(), r['class'])
