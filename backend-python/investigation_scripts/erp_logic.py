# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    
    out.write("=== ERP ORDER LOGIC ANALYSIS ===\n\n")

    # 1. Let's find an order that has partial or full delivery (sat_miq > 0)
    q1 = """
        SELECT TOP 1 e.idn, e.es_no, e.mal, e.miqdar, e.sat_miq
        FROM sm_sif_sened_el e
        WHERE e.sat_miq > 0 AND e.sat_miq < e.miqdar
    """
    partial_order = query(q1)
    
    if partial_order:
        p = partial_order[0]
        out.write(f"Found partially delivered Order Line in sm_sif_sened_el:\n")
        out.write(f"ID: {p['idn']}, Order Header: {p['es_no']}, Product: {p['mal']}, Ordered: {p['miqdar']}, Delivered (sat_miq): {p['sat_miq']}\n\n")
        
        # Let's see if there is an invoice (sm_kontr_sat) linked to this es_no (sif_sen = es_no)
        q2 = f"""
            SELECT s.idn as invoice_id, s.tarix, e.miqdar as invoiced_qty
            FROM sm_kontr_sat s
            JOIN sm_kontr_sat_el e ON s.idn = e.es_no
            WHERE s.sif_sen = {p['es_no']} AND e.mal = {p['mal']}
        """
        invoices = query(q2)
        out.write(f"Invoices linked to this Order (s.sif_sen = {p['es_no']}):\n")
        for inv in invoices:
            out.write(f" - Invoice ID: {inv['invoice_id']}, Date: {inv['tarix']}, Invoiced Qty: {inv['invoiced_qty']}\n")
        out.write("\n")
    
    # 2. Check for SQL Triggers on sm_kontr_sat_el (Invoices)
    # This will show us if the database automatically updates sat_miq when an invoice is saved.
    q3 = """
        SELECT tr.name AS trigger_name, m.definition
        FROM sys.triggers tr
        JOIN sys.sql_modules m ON tr.object_id = m.object_id
        WHERE tr.parent_class_desc = 'OBJECT_OR_COLUMN' 
        AND OBJECT_NAME(tr.parent_id) = 'sm_kontr_sat_el'
    """
    triggers = query(q3)
    out.write("Triggers on Sales Invoice (sm_kontr_sat_el):\n")
    if triggers:
        for t in triggers:
            # We don't want to print the massive code, just look for mentions of sm_sif_sened
            has_update = 'UPDATE sm_sif_sened_el' in t['definition'] or 'sat_miq' in t['definition']
            out.write(f" - Trigger: {t['trigger_name']} (Updates sm_sif_sened_el? {has_update})\n")
    else:
        out.write(" - No triggers found.\n")

    out.write("\n3. Check for Triggers on sm_sif_sened_el (Orders)\n")
    q4 = """
        SELECT tr.name AS trigger_name, m.definition
        FROM sys.triggers tr
        JOIN sys.sql_modules m ON tr.object_id = m.object_id
        WHERE tr.parent_class_desc = 'OBJECT_OR_COLUMN' 
        AND OBJECT_NAME(tr.parent_id) = 'sm_sif_sened_el'
    """
    order_triggers = query(q4)
    if order_triggers:
        for t in order_triggers:
            has_qaliq = 'qaliq' in t['definition']
            out.write(f" - Trigger: {t['trigger_name']} (Updates qaliq? {has_qaliq})\n")
    else:
        out.write(" - No triggers found.\n")

    with io.open("erp_logic.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
