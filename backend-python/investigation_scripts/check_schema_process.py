import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings') # Assuming this is the project
try:
    django.setup()
except Exception as e:
    # Fallback to manual connection
    pass

from dashboard.erp_connector import query

def check_schema():
    print("sm_process_iz columns:")
    try:
        cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_process_iz'")
        print([c['COLUMN_NAME'] for c in cols])
        cols2 = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_process_iz_toxuma'")
        print("toxuma:", [c['COLUMN_NAME'] for c in cols2])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_schema()
