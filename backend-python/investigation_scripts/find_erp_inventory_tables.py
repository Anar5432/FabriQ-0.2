import os, django, sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.erp_connector import query

def check():
    sql = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME LIKE '%qaliq%' 
       OR TABLE_NAME LIKE '%stok%' 
       OR TABLE_NAME LIKE '%rezerv%'
       OR TABLE_NAME LIKE '%anbar%'
       OR TABLE_NAME LIKE '%qabul%'
       OR TABLE_NAME LIKE '%inv%'
       OR TABLE_NAME LIKE '%balans%'
       OR TABLE_NAME LIKE '%sm_mal%'
    """
    res = query(sql)
    print("Tables related to inventory/stock:")
    for r in res:
        print(r['TABLE_NAME'])

if __name__ == '__main__':
    check()
