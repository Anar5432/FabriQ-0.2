import os, django, sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.erp_connector import query

print(query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%silinme%' OR TABLE_NAME LIKE '%alis%' OR TABLE_NAME LIKE '%anbar%' OR TABLE_NAME LIKE '%xerc%'"))
