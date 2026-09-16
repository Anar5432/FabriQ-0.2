import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

def print_columns(table):
    try:
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
        cols = cursor.fetchall()
        print(f"--- {table} ---")
        for c in cols:
            print(f"  {c[0]} ({c[1]})")
        print()
    except Exception as e:
        print(f"Error describing {table}: {e}")

tables = [
    'sm_process_iz',
    'sm_process_iz_toxuma',
    'sm_process_iz_rosso',
    'sm_process_iz_utu',
    'sm_process_iz_yuma',
    'sm_process_iz_etiket',
    'sm_process_iz_qab'
]

for t in tables:
    print_columns(t)

conn.close()
