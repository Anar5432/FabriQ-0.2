import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
from dashboard.erp_connector import query
import json
tables = query('SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE ''%sifaris%''')
for row in tables:
    print(row['TABLE_NAME'])
