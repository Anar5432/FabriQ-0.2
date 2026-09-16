import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

# Get columns of sm_smeta
cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_smeta'")
columns = [row[0] for row in cursor.fetchall()]
print(f"sm_smeta columns: {columns}")

# Also get columns of sm_sifaris_form
cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris_form'")
sifaris_cols = [row[0] for row in cursor.fetchall()]
print(f"sm_sifaris_form columns: {sifaris_cols}")

conn.close()
