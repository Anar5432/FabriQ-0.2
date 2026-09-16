import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

# Check tables with smeta
cursor.execute("SELECT name FROM sys.tables WHERE name LIKE '%smeta%'")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables with 'smeta': {tables}")

# Check columns of sm_smeta_mal if exists
if 'sm_smeta_mal' in tables:
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_smeta_mal'")
    print(f"sm_smeta_mal columns: {[row[0] for row in cursor.fetchall()]}")

if 'sm_smeta_isci' in tables:
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_smeta_isci'")
    print(f"sm_smeta_isci columns: {[row[0] for row in cursor.fetchall()]}")

conn.close()
