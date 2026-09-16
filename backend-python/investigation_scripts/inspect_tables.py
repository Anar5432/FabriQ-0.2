# -*- coding: utf-8 -*-
import sys, os, django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

def inspect_table(table_name):
    print(f"\n========== TABLE: {table_name} ==========")
    try:
        # Get one recent row to see data types and populated fields
        sql = f"SELECT TOP 1 * FROM {table_name} WITH (NOLOCK) ORDER BY idn DESC"
        rows = query(sql)
        if not rows:
            print("Table is empty.")
            return
            
        row = rows[0]
        # Just print keys and their type / sample value
        for key, val in row.items():
            val_preview = str(val)[:50] if val is not None else 'NULL'
            print(f" - {key}: {val_preview}")
            
    except Exception as e:
        print(f"Error inspecting {table_name}: {e}")

if __name__ == '__main__':
    tables = [
        # Stage 0: Sales Order
        'sm_sif_sened',      # Isci Order Header
        'sm_sif_sened_el',   # Isci Order Lines
        'sm_kontr_sat',      # Corab Order Header
        'sm_kontr_sat_el',   # Corab Order Lines
        
        # Stage X: Production Document (Smeta)
        'sm_good_ist',       # Prod Header
        'sm_good_ist_el',    # Prod Lines
        
        # Stage 1-5: Department Transfers
        'sm_sob_trans',      # Transfer Header
        'sm_sob_trans_el'    # Transfer Lines
    ]
    
    for t in tables:
        inspect_table(t)
