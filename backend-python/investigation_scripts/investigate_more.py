import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

with open('investigation_results2.txt', 'w', encoding='utf-8') as f:
    
    # 1. Salary Check
    try:
        sql_maas = "SELECT COUNT(*) as cnt, MAX(tarix) as last_date FROM sm_maas_hes"
        maas = query(sql_maas)[0]
        f.write(f"Salaries (sm_maas_hes) -> Total Records: {maas['cnt']}, Last entry: {maas['last_date']}\n")
    except Exception as e:
        f.write(f"Error querying sm_maas_hes: {e}\n")

    # 2. Expense Categories
    try:
        sql_xerc_cats = "SELECT * FROM xerc_maddeleri"
        cats = query(sql_xerc_cats)
        f.write(f"\nExpense Categories (xerc_maddeleri):\n")
        for c in cats:
            f.write(f"{c}\n")
    except Exception as e:
        f.write(f"Error querying xerc_maddeleri: {e}\n")

    # 3. KMX (Outgoing cash)
    try:
        sql_kmx = """
        SELECT TOP 5 k.idn, k.tarix, k.mebleg, k.kontra, c.name as kontra_name 
        FROM sm_kmx k
        LEFT JOIN sm_kontra c ON k.kontra = c.idn
        ORDER BY k.tarix DESC
        """
        f.write("\nOutgoing Cash (sm_kmx):\n")
        for r in query(sql_kmx):
            f.write(f"{r}\n")
            
        sql_kmx_count = "SELECT COUNT(*) as cnt, MAX(tarix) as last_date FROM sm_kmx"
        kmx_cnt = query(sql_kmx_count)[0]
        f.write(f"\nTotal Outgoing Cash (sm_kmx): {kmx_cnt['cnt']} entries, last on {kmx_cnt['last_date']}\n")
    except Exception as e:
        f.write(f"Error querying sm_kmx: {e}\n")

    # 4. Contractor Types
    try:
        sql_k_types = """
        SELECT nov, COUNT(*) as cnt FROM sm_kontra GROUP BY nov
        """
        f.write(f"\nContractor Types (nov):\n")
        for r in query(sql_k_types):
            f.write(f"{r}\n")

        sql_k_types2 = """
        SELECT mus_nov, COUNT(*) as cnt FROM sm_kontra GROUP BY mus_nov
        """
        f.write(f"\nCustomer Types (mus_nov):\n")
        for r in query(sql_k_types2):
            f.write(f"{r}\n")
    except Exception as e:
        f.write(f"Error querying contractor types: {e}\n")
