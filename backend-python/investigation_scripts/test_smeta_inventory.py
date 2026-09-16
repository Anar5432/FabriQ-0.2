import sys
import os
from collections import defaultdict
import copy

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def test_smeta_inventory():
    print("--- Fetching Product SMETA Requirements ---")
    sql_req = """
    SELECT 
        satis.mal AS hm_product_id,
        xammal.mal AS raw_material_id,
        MAX(g.name) AS raw_material_name,
        MAX(xammal.miqdar) AS qty_per_unit
    FROM sm_smeta_satis satis WITH (NOLOCK)
    JOIN (
        SELECT mal, MAX(es_no) as latest_smeta_id
        FROM sm_smeta_satis s WITH (NOLOCK)
        JOIN sm_smeta sm WITH (NOLOCK) ON s.es_no = sm.idn
        WHERE sm.tesdiq = 1
        GROUP BY mal
    ) latest ON satis.mal = latest.mal AND satis.es_no = latest.latest_smeta_id
    JOIN sm_smeta_xammal xammal WITH (NOLOCK) ON satis.es_no = xammal.es_no
    JOIN sm_goods g WITH (NOLOCK) ON xammal.mal = g.idn
    GROUP BY satis.mal, xammal.mal
    """
    req_raw = query(sql_req)
    smeta_reqs = defaultdict(list)
    all_needed_materials = set()
    for r in req_raw:
        smeta_reqs[r['hm_product_id']].append({
            'mat_id': r['raw_material_id'],
            'mat_name': r['raw_material_name'],
            'qty_per_unit': float(r['qty_per_unit'])
        })
        all_needed_materials.add(r['raw_material_id'])

    mat_list = ",".join(str(m) for m in all_needed_materials)

    print("\n--- Fetching Global Inventory for required materials ---")
    # Global balance: all INs minus all OUTs across the whole system
    sql_inv = f"""
    SELECT 
        dept_id, mal, SUM(balance) as balance
    FROM (
        SELECT 
            ISNULL(ins.dept_id, outs.dept_id) as dept_id,
            ISNULL(ins.mal, outs.mal) as mal,
            ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) as balance
        FROM (
            SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in
            FROM sm_sob_trans t WITH (NOLOCK)
            JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
            WHERE t.tesdiq = 1 AND tel.mal IN ({mat_list}) AND t.sobe2 IS NOT NULL
            GROUP BY t.sobe2, tel.mal
        ) ins
        FULL OUTER JOIN (
            SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
            FROM sm_sob_trans t WITH (NOLOCK)
            JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
            WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL AND tel.mal IN ({mat_list})
            GROUP BY t.sobe1, tel.mal
        ) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
    ) bal
    WHERE balance > 0
    GROUP BY dept_id, mal
    """
    inventory_raw = query(sql_inv)
    # Sum across all departments to get a single global pool
    global_inventory = defaultdict(float)
    for row in inventory_raw:
        global_inventory[row['mal']] += float(row['balance'])
        
    print(f"Loaded {len(global_inventory)} materials currently in stock globally.")

    print("\n--- Fetching Active Orders (FIFO simulation) ---")
    cls = "(27)" # isci
    sql_orders = f"""
    SELECT
        s.idn AS order_id,
        s.kontra_name AS company_name,
        e.idn AS line_id,
        g.idn AS product_id,
        g.name AS product_name,
        e.miqdar AS qty_ordered,
        e.qaliq AS qty_remaining,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix
    FROM sm_kontr_sat s WITH (NOLOCK)
    JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE g.class IN {cls}
      AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    ORDER BY s.tarix ASC, e.num
    """
    orders = query(sql_orders)
    
    virtual_inventory = copy.deepcopy(global_inventory)
    
    results = []
    
    for o in orders:
        qaliq = float(o['qty_remaining'] or 0)
        if qaliq == 0:
            continue
            
        pid = o['product_id']
        if pid not in smeta_reqs:
            results.append({
                'order': o,
                'readiness': 0,
                'missing': [{'mat_name': 'No SMETA found for product', 'needed': 0, 'missing': 0}]
            })
            continue
            
        reqs = smeta_reqs[pid]
        missing_materials = []
        total_items = len(reqs)
        items_ready = 0
        
        for r in reqs:
            mat_id = r['mat_id']
            needed_qty = r['qty_per_unit'] * qaliq
            avail_qty = virtual_inventory.get(mat_id, 0)
            
            if avail_qty >= needed_qty:
                virtual_inventory[mat_id] -= needed_qty
                items_ready += 1
            else:
                missing_qty = needed_qty - avail_qty
                virtual_inventory[mat_id] = 0
                missing_materials.append({
                    'mat_name': r['mat_name'],
                    'needed': needed_qty,
                    'missing': missing_qty
                })
        
        readiness_percentage = int((items_ready / total_items) * 100) if total_items > 0 else 0
        
        results.append({
            'order': o,
            'readiness': readiness_percentage,
            'missing': missing_materials
        })

    with open("smeta_results.txt", "w", encoding="utf-8") as f:
        for r in results:
            if r['readiness'] > 0 and r['readiness'] < 100:
                f.write(f"Order: {r['order']['company_name']} - {r['order']['product_name']} ({r['order']['qty_remaining']} pcs)\n")
                f.write(f"Readiness: {r['readiness']}%\n")
                for m in r['missing']:
                    f.write(f"  -> Missing: {m['mat_name']} | Need: {m['needed']} | Missing: {m['missing']}\n")
                f.write("\n")
                
        f.write("=== 100% READY ORDERS ===\n")
        ready_count = sum(1 for r in results if r['readiness'] == 100)
        f.write(f"Count: {ready_count}\n")
        
        f.write("=== 0% READY ORDERS ===\n")
        zero_count = sum(1 for r in results if r['readiness'] == 0 and r['missing'][0]['mat_name'] != 'No SMETA found for product')
        f.write(f"Count: {zero_count}\n")
        
        f.write("=== NO SMETA ORDERS ===\n")
        nosmeta_count = sum(1 for r in results if r['missing'] and r['missing'][0]['mat_name'] == 'No SMETA found for product')
        f.write(f"Count: {nosmeta_count}\n")
        
    print("Check smeta_results.txt")

if __name__ == "__main__":
    test_smeta_inventory()
