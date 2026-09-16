import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def main():
    print("--- 1. Fetching Open Orders ---")
    sql_active = """
    SELECT 
        ISNULL(s.sifaris, s.idn) AS order_id,
        s.sen_no,
        CONVERT(VARCHAR(10), s.tarix, 23) as tarix,
        e.idn AS line_id,
        g.idn AS product_id,
        g.name AS product_name,
        e.miqdar AS qty_ordered,
        e.miqdar AS qty_remaining
    FROM sm_sifaris_form s WITH (NOLOCK)
    JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE e.miqdar > 0
      AND s.tarix >= DATEADD(MONTH, -6, GETDATE())
    UNION ALL
    SELECT 
        s.idn AS order_id,
        s.sen_no,
        CONVERT(VARCHAR(10), s.tarix, 23) as tarix,
        e.idn AS line_id,
        g.idn AS product_id,
        g.name AS product_name,
        e.miqdar AS qty_ordered,
        (e.miqdar - ISNULL(e.sat_miq, 0)) AS qty_remaining
    FROM sm_sif_sened s WITH (NOLOCK)
    JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE (e.miqdar - ISNULL(e.sat_miq, 0)) > 0
      AND NOT EXISTS (SELECT 1 FROM sm_sifaris_form sf WITH (NOLOCK) WHERE sf.sifaris = s.idn)
      AND s.tarix >= DATEADD(MONTH, -6, GETDATE())
    """
    orders = query(sql_active)
    print(f"Total Open Order Lines found (last 6 months): {len(orders)}")
    
    print("--- 2. Checking Production Status (Started vs Not Started) ---")
    order_ids = set([str(int(o['order_id'])) for o in orders])
    
    if not order_ids:
        print("No orders to check.")
        return

    order_ids_str = ",".join(order_ids)
    
    sql_started_corab = f"""
    SELECT DISTINCT i.sif_no as order_id
    FROM sm_good_ist i WITH (NOLOCK)
    WHERE i.sif_no IN ({order_ids_str})
    """
    started_corab = {str(int(r['order_id'])) for r in query(sql_started_corab)}
    
    sql_started_isci = f"""
    SELECT DISTINCT el_sif as order_id
    FROM sm_sob_trans WITH (NOLOCK)
    WHERE el_sif IN ({order_ids_str}) AND tesdiq = 1
    """
    started_isci = {str(int(r['order_id'])) for r in query(sql_started_isci)}
    
    started_all = started_corab.union(started_isci)
    
    not_started_orders = [o for o in orders if str(int(o['order_id'])) not in started_all]
    started_orders = [o for o in orders if str(int(o['order_id'])) in started_all]
    
    print(f"Orders Started Production: {len(started_orders)}")
    print(f"Orders NOT Started (Needs Planning): {len(not_started_orders)}")
    
    print("\\n--- 3. Checking SMETA (BOM/Routing) Document completeness ---")
    product_ids = list(set([str(int(o['product_id'])) for o in orders]))
    if not product_ids:
        return
        
    pids_str = ",".join(product_ids)
    
    sql_smeta_map = f"""
    SELECT s.mal as product_id, sm.idn as smeta_id, sm.sen_no, sm.tesdiq
    FROM sm_smeta_satis s WITH (NOLOCK)
    JOIN sm_smeta sm WITH (NOLOCK) ON s.es_no = sm.idn
    WHERE s.mal IN ({pids_str}) AND sm.tesdiq = 1
    """
    smeta_map_raw = query(sql_smeta_map)
    
    product_to_smeta = {}
    smeta_ids = set()
    for r in smeta_map_raw:
        pid = str(int(r['product_id']))
        sid = str(int(r['smeta_id']))
        product_to_smeta[pid] = sid
        smeta_ids.add(sid)
        
    print(f"Products with an approved SMETA: {len(product_to_smeta)} / {len(product_ids)}")
    
    if not smeta_ids:
        print("No SMETAs found.")
        return
        
    sids_str = ",".join(smeta_ids)
    
    sql_xammal = f"SELECT DISTINCT es_no FROM sm_smeta_xammal WITH (NOLOCK) WHERE es_no IN ({sids_str})"
    smetas_with_materials = {str(int(r['es_no'])) for r in query(sql_xammal)}
    
    sql_xerc = f"SELECT DISTINCT es_no FROM sm_smeta_xerc WITH (NOLOCK) WHERE es_no IN ({sids_str})"
    smetas_with_operations = {str(int(r['es_no'])) for r in query(sql_xerc)}
    
    sql_xerc_cost = f"SELECT DISTINCT es_no FROM sm_smeta_xerc WITH (NOLOCK) WHERE es_no IN ({sids_str}) AND ISNULL(mebleg, 0) > 0"
    smetas_with_costs = {str(int(r['es_no'])) for r in query(sql_xerc_cost)}
    
    def calc_stats(order_list):
        total = len(order_list)
        if total == 0: return {}
        
        has_smeta = 0
        has_mat = 0
        has_ops = 0
        has_cost = 0
        
        for o in order_list:
            pid = str(int(o['product_id']))
            if pid in product_to_smeta:
                has_smeta += 1
                sid = product_to_smeta[pid]
                if sid in smetas_with_materials: has_mat += 1
                if sid in smetas_with_operations: has_ops += 1
                if sid in smetas_with_costs: has_cost += 1
                
        return {
            'total': total,
            'has_smeta': has_smeta,
            'pct_smeta': (has_smeta/total)*100,
            'missing_mat': has_smeta - has_mat,
            'missing_ops': has_smeta - has_ops,
            'missing_cost': has_smeta - has_cost,
            'pct_missing_mat': ((has_smeta - has_mat)/has_smeta)*100 if has_smeta > 0 else 0,
            'pct_missing_ops': ((has_smeta - has_ops)/has_smeta)*100 if has_smeta > 0 else 0,
            'pct_missing_cost': ((has_smeta - has_cost)/has_smeta)*100 if has_smeta > 0 else 0
        }
        
    overall_stats = calc_stats(orders)
    not_started_stats = calc_stats(not_started_orders)
    
    print("\\n--- STATS: ALL OPEN ORDERS ---")
    print(f"Total: {overall_stats.get('total', 0)}")
    if overall_stats:
        print(f"Has SMETA: {overall_stats['has_smeta']} ({overall_stats['pct_smeta']:.1f}%)")
        if overall_stats['has_smeta'] > 0:
            print(f"  Missing Materials: {overall_stats['missing_mat']} ({overall_stats['pct_missing_mat']:.1f}%)")
            print(f"  Missing Operations: {overall_stats['missing_ops']} ({overall_stats['pct_missing_ops']:.1f}%)")
            print(f"  Missing Costs/Wages: {overall_stats['missing_cost']} ({overall_stats['pct_missing_cost']:.1f}%)")
        
    print("\\n--- STATS: ORDERS NOT YET STARTED (TARGET FOR PLANNING) ---")
    print(f"Total: {not_started_stats.get('total', 0)}")
    if not_started_stats:
        print(f"Has SMETA: {not_started_stats['has_smeta']} ({not_started_stats['pct_smeta']:.1f}%)")
        if not_started_stats['has_smeta'] > 0:
            print(f"  Missing Materials: {not_started_stats['missing_mat']} ({not_started_stats['pct_missing_mat']:.1f}%)")
            print(f"  Missing Operations: {not_started_stats['missing_ops']} ({not_started_stats['pct_missing_ops']:.1f}%)")
            print(f"  Missing Costs/Wages: {not_started_stats['missing_cost']} ({not_started_stats['pct_missing_cost']:.1f}%)")
        
    print("\\n--- REAL EXAMPLES OF PRODUCTS WITH MISSING DATA ---")
    examples_found = 0
    for o in not_started_orders:
        if examples_found >= 2: break
        pid = str(int(o['product_id']))
        if pid in product_to_smeta:
            sid = product_to_smeta[pid]
            has_ops = sid in smetas_with_operations
            has_cost = sid in smetas_with_costs
            if not has_ops or not has_cost:
                print(f"Example: Order {o['sen_no']} - Product: {o['product_name']} (ID: {pid})")
                print(f"  -> SMETA ID: {sid}")
                print(f"  -> Has Materials: {sid in smetas_with_materials}")
                print(f"  -> Has Operations Assigned: {has_ops}")
                print(f"  -> Has Operation Cost/Wage: {has_cost}\\n")
                examples_found += 1

if __name__ == '__main__':
    main()
