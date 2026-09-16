import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()

cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = [row[0] for row in cursor.fetchall()]

keywords = ['kesim', 'tikis', 'hisse', 'emeliyyat', 'proses', 'is_', 'stage', 'process']
found_tables = []
for t in tables:
    for k in keywords:
        if k in t.lower():
            found_tables.append(t)
            break

print("Tables matching keywords:", found_tables)

# For sm_smeta_xidmet, let's see what xidmet=11 actually is.
cursor.execute("SELECT * FROM sm_xidmet WHERE idn=11")
try:
    print("sm_xidmet 11:", cursor.fetchone())
except:
    pass

cursor.execute("SELECT * FROM sm_goods WHERE idn=11")
try:
    print("sm_goods 11:", cursor.fetchone())
except:
    pass

# Check if there is any other table linked to sm_smeta (es_no)
smeta_linked = []
for t in tables:
    try:
        cursor.execute(f"SELECT TOP 1 es_no FROM {t}")
        smeta_linked.append(t)
    except:
        pass
print("Tables with es_no:", smeta_linked)

conn.close()
