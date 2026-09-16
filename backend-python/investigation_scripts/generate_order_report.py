import os
import django
import sys
import codecs

# Fix console encoding for Azerbaijani characters
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def generate_report():
    print("## Production Status: Recent 20 Orders")
    print("| Order ID | Order No | Customer | Total Qty | Knitting (`toxuma`) | Sewing (`rosso`) | Washing (`yuma`) | Ironing (`utu`) |")
    print("|---|---|---|---|---|---|---|---|")
    
    try:
        # Get 20 recent orders
        orders = query("""
            SELECT TOP 20 s.idn, s.sen_no, s.tarix, c.name as customer, SUM(e.miqdar) as total_qty
            FROM sm_sifaris_form s 
            JOIN sm_sifaris_form_el e ON e.es_no = s.idn
            LEFT JOIN sm_kontra c ON s.kontra = c.idn
            WHERE EXISTS (SELECT 1 FROM sm_process_iz p WHERE p.sifaris = s.idn)
            GROUP BY s.idn, s.sen_no, s.tarix, c.name
            ORDER BY s.idn DESC
        """)
        
        for o in orders:
            sif_id = o['idn']
            sen_no = o.get('sen_no', 'N/A')
            customer = o.get('customer', 'Unknown') or 'Unknown'
            total_qty = o.get('total_qty', 0)
            
            # Find the process ticket for this order
            proc = query(f"SELECT idn FROM sm_process_iz WHERE sifaris = {sif_id}")
            if not proc:
                print(f"| {sif_id} | {sen_no} | {customer} | {total_qty} | *Not Started* | *Not Started* | *Not Started* | *Not Started* |")
                continue
                
            proc_id = proc[0]['idn']
            
            # Helper to get qty from a specific stage table
            def get_stage_qty(table_name):
                q = query(f"SELECT SUM(miqdar) as stage_qty FROM {table_name} WHERE es_no = {proc_id}")
                return q[0]['stage_qty'] if q and q[0]['stage_qty'] is not None else 0
                
            toxuma_qty = get_stage_qty('sm_process_iz_toxuma')
            rosso_qty = get_stage_qty('sm_process_iz_rosso')
            yuma_qty = get_stage_qty('sm_process_iz_yuma')
            utu_qty = get_stage_qty('sm_process_iz_utu')
            
            print(f"| {sif_id} | {sen_no} | {customer} | {total_qty} | {toxuma_qty} | {rosso_qty} | {yuma_qty} | {utu_qty} |")
            
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    generate_report()
