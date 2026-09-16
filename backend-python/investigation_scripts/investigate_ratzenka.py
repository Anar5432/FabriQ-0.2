import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def investigate():
    print("Fetching a sample rasenka...")
    res = query("SELECT TOP 1 idn, sen_no, sif_sen FROM sm_rasenka ORDER BY idn DESC")
    if not res:
        print("No rasenka found.")
        return
    
    r_id = res[0]['idn']
    print(f"Sample Rasenka: {res[0]}")
    
    print("\n--- sm_rasenka_el (Processes?) ---")
    el_res = query(f"SELECT * FROM sm_rasenka_el WHERE es_no = {r_id}")
    for row in el_res[:5]: print(row) # print only top 5 to avoid clutter
    
    print("\n--- sm_rasenka_el_el (Worker assignment?) ---")
    el_el_res = query(f"SELECT * FROM sm_rasenka_el_el WHERE es_no = {r_id}")
    for row in el_el_res[:5]: print(row)
    
    print("\n--- sm_rasenka_emp (Worker Header?) ---")
    emp_res = query(f"SELECT * FROM sm_rasenka_emp WHERE sen_no = '{res[0]['sen_no']}' OR idn = {r_id}")
    for row in emp_res[:5]: print(row)
    
    print("\n--- sm_rasenka_emp_el (Worker Groups?) ---")
    emp_el_res = query(f"SELECT * FROM sm_rasenka_emp_el WHERE es_no = {r_id}")
    for row in emp_el_res[:5]: print(row)
    
    print("\n--- sm_rasenka_emp_el_el (Worker processes?) ---")
    emp_el_el_res = query(f"SELECT * FROM sm_rasenka_emp_el_el WHERE es_no = {r_id}")
    for row in emp_el_el_res[:5]: print(row)

if __name__ == '__main__':
    investigate()
