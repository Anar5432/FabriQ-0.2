import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_borc'"
print(query(sql))

# Get a sample row from sm_borc
sql_sample = "SELECT TOP 1 * FROM sm_borc"
print(query(sql_sample))
