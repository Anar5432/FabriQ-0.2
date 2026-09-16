import os, django, sys
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.erp_connector import query

def check_tables():
    # Find all tables with 'mal', 'stok', 'sened', 'silinme', 'anbar', 'hereket'
    sql = """
    SELECT TABLE_NAME, TABLE_TYPE 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME LIKE '%mal%' 
       OR TABLE_NAME LIKE '%stok%'
       OR TABLE_NAME LIKE '%sened%'
       OR TABLE_NAME LIKE '%anbar%'
       OR TABLE_NAME LIKE '%sil%'
       OR TABLE_NAME LIKE '%xerc%'
       OR TABLE_NAME LIKE '%qaliq%'
       OR TABLE_NAME LIKE '%sob_trans%'
    """
    tables = query(sql)
    
    # We want to see row counts for the most promising tables to understand which ones are heavily used.
    # Promising tables are usually the transaction ledgers.
    target_keywords = ['hes', 'sil', 'teleb', 'sened', 'trans', 'qaliq', 'stok']
    
    print("--- DEEP DB ANALYSIS ---")
    promising_tables = []
    for t in tables:
        tname = t['TABLE_NAME'].lower()
        if any(k in tname for k in target_keywords) and not tname.startswith('v_') and not tname.endswith('_log'):
            promising_tables.append(t['TABLE_NAME'])
            
    print(f"Found {len(promising_tables)} promising tables. Checking row counts for a subset...")
    
    # Check row counts for a focused subset
    subset = [
        'sm_mal_hes', 'sm_mal_sil', 'sm_telebname_anbar', 'sm_telebname_anbar_el', 
        'sm_sened', 'sm_sened_el', 'sm_sob_trans', 'sm_sob_trans_el',
        'sm_mal_qaliq', 'sm_stok', 'sm_mal_hereket', 'sm_silinme'
    ]
    
    for tname in subset:
        try:
            res = query(f"SELECT COUNT(*) as c FROM {tname}")
            print(f"Table {tname}: {res[0]['c']} rows")
        except Exception as e:
            # Table might not exist or error
            pass
            
    # Check what columns sm_sob_trans and sm_sened_el have to see if they are the true ledger
    try:
        cols_trans = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sob_trans_el'")
        print(f"\\nsm_sob_trans_el cols: {[c['COLUMN_NAME'] for c in cols_trans]}")
    except: pass
    
    try:
        cols_sened = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sened_el'")
        print(f"\\nsm_sened_el cols: {[c['COLUMN_NAME'] for c in cols_sened]}")
    except: pass
    
    try:
        cols_mal = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_mal_hes'")
        print(f"\\nsm_mal_hes cols: {[c['COLUMN_NAME'] for c in cols_mal]}")
    except: pass

if __name__ == '__main__':
    check_tables()
