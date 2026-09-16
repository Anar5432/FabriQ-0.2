import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def find_workers():
    res = query("""
        SELECT p.name, COUNT(*) as c 
        FROM sm_emp e 
        LEFT JOIN sm_position p ON e.position = p.idn
        WHERE e.ise_son IS NULL 
        GROUP BY p.name 
        ORDER BY c DESC
    """)
    print("\nPositions:")
    for r in res[:20]:
        print(r)

if __name__ == '__main__':
    find_workers()
