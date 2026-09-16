import os
import sys
import django
import copy
import datetime
import hashlib
from collections import defaultdict

# Must setup django before importing dashboard modules
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
    django.setup()

from dashboard.erp_connector import query
from dashboard.queries import get_orders
from dashboard.material_checker import extract_colors

def add_working_minutes(start_dt, minutes):
    """
    Adds working minutes to a datetime, respecting 09:00 - 18:00 (with 1 hr lunch = 8 working hours).
    If time goes past 18:00, it spills over to 09:00 the next day.
    """
    current_dt = start_dt
    
    # If the start time is before 9am, snap to 9am
    if current_dt.hour < 9:
        current_dt = current_dt.replace(hour=9, minute=0, second=0, microsecond=0)
    
    # If the start time is during lunch (13:00 - 14:00), push to 14:00
    if 13 <= current_dt.hour < 14:
        current_dt = current_dt.replace(hour=14, minute=0, second=0, microsecond=0)
        
    # If the start time is after 18:00, snap to 9am next day
    if current_dt.hour >= 18:
        current_dt = current_dt.replace(hour=9, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        
    remaining_minutes = minutes
    
    while remaining_minutes > 0:
        # Calculate how many minutes are left in the current shift
        if current_dt.hour < 13:
            end_of_block = current_dt.replace(hour=13, minute=0)
        else:
            end_of_block = current_dt.replace(hour=18, minute=0)
            
        available_minutes_in_block = (end_of_block - current_dt).total_seconds() / 60.0
        
        if remaining_minutes <= available_minutes_in_block:
            current_dt += datetime.timedelta(minutes=remaining_minutes)
            remaining_minutes = 0
            
            # Snap out of lunch break if we land exactly at 13:00
            if current_dt.hour == 13 and current_dt.minute == 0:
                current_dt = current_dt.replace(hour=14, minute=0)
            # Snap to next day if we land exactly at 18:00
            elif current_dt.hour == 18 and current_dt.minute == 0:
                current_dt = current_dt.replace(hour=9, minute=0) + datetime.timedelta(days=1)
                
        else:
            remaining_minutes -= available_minutes_in_block
            if current_dt.hour < 13:
                # Move past lunch
                current_dt = current_dt.replace(hour=14, minute=0)
            else:
                # Move to next day
                current_dt = current_dt.replace(hour=9, minute=0) + datetime.timedelta(days=1)
                
    return current_dt

class Worker:
    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name
        self.process_groups = set()
        
        # Start availability at 09:00 today
        now = datetime.datetime.now()
        self.available_from = datetime.datetime(now.year, now.month, now.day, 9, 0)
        self.capacities = {} # op_id -> avg_daily_power

    def __repr__(self):
        return f"<Worker {self.emp_id}: {self.name} | Groups: {len(self.process_groups)}>"

class Order:
    def __init__(self, idn, sen_no, product_id, product_name, qty, date_created, order_id=None):
        self.idn = idn
        self.sen_no = sen_no
        self.product_id = product_id
        self.product_name = product_name
        self.qty = float(qty)
        self.date_created = date_created
        self.order_id = order_id
        self.missing_materials = []

    def __repr__(self):
        return f"<Order {self.sen_no} | Product: {self.product_id} | Qty: {self.qty}>"

class PlanningEngine:
    def __init__(self):
        self.workers = {}
        self.active_orders = []
        self.inventory = defaultdict(float) # mat_id -> qty available (FIFO calculated)
        self.material_names = {} # mat_id -> mat_name
        self.smeta_reqs = defaultdict(list) # product_id -> list of dicts with mat_id, qty_per_unit
        self._ops_cache = {} # order_id -> operations
        
    def load_workers(self):
        sql = """
        WITH WorkerDaily AS (
            SELECT 
                e.emp,
                MAX(e.emp_name) as emp_name,
                r.tarix,
                r_el.xidmet as op_id,
                SUM(e.miqdar) as daily_miqdar
            FROM sm_rasenka_el_el e WITH (NOLOCK)
            JOIN sm_rasenka_el r_el WITH (NOLOCK) ON e.es_no = r_el.es_no AND e.el_no = r_el.idn
            JOIN sm_rasenka r WITH (NOLOCK) ON r_el.es_no = r.idn
            WHERE e.emp IS NOT NULL
            GROUP BY e.emp, r.tarix, r_el.xidmet
        )
        SELECT 
            emp,
            MAX(emp_name) as emp_name,
            op_id,
            AVG(CAST(daily_miqdar AS FLOAT)) as capacity
        FROM WorkerDaily
        GROUP BY emp, op_id
        """
        for r in query(sql, cache_key='planning_engine_workers_v3', cache_ttl=3600):
            emp_id = r['emp']
            if emp_id not in self.workers:
                w = Worker(emp_id, r['emp_name'])
                self.workers[emp_id] = w
            
            op_id = r['op_id']
            self.workers[emp_id].process_groups.add(op_id)
            if r['capacity']:
                self.workers[emp_id].capacities[op_id] = float(r['capacity'])
                
        print(f"Loaded {len(self.workers)} workers.")

    def load_inventory_and_backlog(self, sector='isci', target_order_id=None):
        """Loads all active orders (FIFO backlog) and calculates the remaining raw material stock."""
        from collections import defaultdict
        # Fetch all active orders across all categories
        active_orders_sql = '''
        SELECT 
            s.idn AS order_id,
            s.sen_no,
            s.tarix,
            e.idn AS line_id,
            g.class,
            g.idn AS product_id,
            g.name AS product_name,
            (e.miqdar - ISNULL(e.sat_miq, 0)) AS qty_remaining
        FROM sm_sif_sened s WITH (NOLOCK)
        JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
        JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
        WHERE (e.miqdar - ISNULL(e.sat_miq, 0)) > 0
          AND s.tarix >= '2023-01-01'
          AND g.class IN (18, 20, 21, 29, 30, 22, 24, 27, 31, 32, 34)
        ORDER BY s.tarix ASC
        '''
        raw_orders = query(active_orders_sql)
        self.active_orders = []
        for o in raw_orders:
            qty = float(o['qty_remaining'])
            if qty > 0:
                self.active_orders.append(Order(
                    idn=o['line_id'],
                    sen_no=o['sen_no'],
                    product_id=str(o['product_id']),
                    product_name=o['product_name'],
                    qty=qty,
                    date_created=o['tarix'],
                    order_id=o['order_id']
                ))

        # Sort active orders by date for FIFO
        self.active_orders.sort(key=lambda x: str(x.date_created))
        
        order_ids = [str(o.order_id) for o in self.active_orders]
        if target_order_id and str(target_order_id) not in order_ids:
            order_ids.append(str(target_order_id))

        if not order_ids:
            print("No orders to fetch smeta for.")
            return

        oid_str = ",".join(order_ids)

        # Fetch SMETA requirements via direct order link (sorgu)
        sql_req = f"""
        SELECT 
            sm.sorgu AS order_id, 
            xammal.mal AS raw_material_id,
            MAX(g.name) AS raw_material_name, 
            MAX(xammal.miqdar) AS qty_per_unit
        FROM sm_smeta sm WITH (NOLOCK)
        JOIN sm_smeta_xammal xammal WITH (NOLOCK) ON sm.idn = xammal.es_no
        JOIN sm_goods g WITH (NOLOCK) ON xammal.mal = g.idn
        WHERE sm.sorgu IN ({oid_str})
        GROUP BY sm.sorgu, xammal.mal
        """
        req_raw = query(sql_req)
        all_needed_materials = set()
        
        for r in req_raw:
            order_id = str(r['order_id'])
            mat_id = r['raw_material_id']
            mat_name = r['raw_material_name']
                
            self.smeta_reqs[order_id].append({
                'mat_id': mat_id,
                'mat_name': mat_name,
                'qty_per_unit': float(r['qty_per_unit'])
            })
            all_needed_materials.add(mat_id)
            self.material_names[mat_id] = mat_name

        self.missing_smeta_orders = []
        for o in self.active_orders:
            oid = str(o.order_id)
            if oid not in self.smeta_reqs or not self.smeta_reqs[oid]:
                self.missing_smeta_orders.append({
                    'order_id': o.sen_no,
                    'product_name': o.product_name
                })

        # Pre-fetch operations for all products in these orders in one query to avoid DB hits
        sql_ops = f"""
        SELECT 
            e.mal as product_id,
            gel.idn as op_id,
            MAX(gel.name) as op_name,
            MAX(qrup.name) as group_name
        FROM sm_sif_sened_el e WITH (NOLOCK)
        JOIN sm_good_xidmet gx WITH (NOLOCK) ON e.mal = gx.es_no
        JOIN sm_gel gel WITH (NOLOCK) ON gx.xidmet = gel.idn
        JOIN sm_gel_qrup qrup WITH (NOLOCK) ON gel.qrup = qrup.idn
        WHERE e.es_no IN ({oid_str})
        GROUP BY e.mal, gel.idn
        """
        raw_ops = query(sql_ops)
        
        # Initialize empty dicts based on the returned product_ids
        for r in raw_ops:
            pid = str(r['product_id'])
            if pid not in self._ops_cache:
                self._ops_cache[pid] = {
                    'phase1_prep': [],
                    'phase2_assembly': [],
                    'phase3_finishing': []
                }
            
            op_data = {
                'op_id': r['op_id'],
                'op_name': r['op_name'],
                'group_name': r['group_name']
            }
            group_name = r['group_name']
            
            if group_name == 'Tikiş - Hazırlıq':
                self._ops_cache[pid]['phase1_prep'].append(op_data)
            elif group_name == 'Tikiş - Bədən':
                self._ops_cache[pid]['phase2_assembly'].append(op_data)
            elif group_name in ('Tikiş - Cib', 'Tikiş - Fermuar', 'Tikiş - Digər'):
                self._ops_cache[pid]['phase3_finishing'].append(op_data)
            else:
                self._ops_cache[pid]['phase2_assembly'].append(op_data)

        # Fetch Global Inventory from sm_mal_say
        # raw: 1, 8, 24
        # leftover: 3, 4, 5, 17, 39
        global_inventory = {}
        if all_needed_materials:
            mat_list = ",".join(str(m) for m in all_needed_materials)
            sql_inv = f"""
            SELECT anbar, mal, SUM(miq_el - say_sil) as balance
            FROM sm_mal_say WITH (NOLOCK)
            WHERE mal IN ({mat_list}) AND (miq_el - say_sil) > 0
              AND anbar IN (1, 8, 24, 3, 4, 5, 17, 39)
            GROUP BY anbar, mal
            """
            for row in query(sql_inv):
                mat = row['mal']
                anbar = row['anbar']
                bal = float(row['balance'])
                if mat not in global_inventory:
                    global_inventory[mat] = {'raw': 0.0, 'leftover': 0.0, 'total': 0.0}
                
                if anbar in [1, 8, 24]:
                    global_inventory[mat]['raw'] += bal
                else:
                    global_inventory[mat]['leftover'] += bal
                    
                global_inventory[mat]['total'] += bal

        # Process FIFO Reservation for Backlog
        virtual_inventory = copy.deepcopy(global_inventory)
        for o in self.active_orders:
            reqs = self.smeta_reqs.get(str(o.order_id), [])
            for r in reqs:
                mat_id = r['mat_id']
                needed_qty = r['qty_per_unit'] * o.qty
                
                if mat_id not in virtual_inventory:
                    virtual_inventory[mat_id] = {'raw': 0.0, 'leftover': 0.0, 'total': 0.0}
                
                # Drain raw first, then leftover
                if virtual_inventory[mat_id]['raw'] >= needed_qty:
                    virtual_inventory[mat_id]['raw'] -= needed_qty
                else:
                    rem = needed_qty - virtual_inventory[mat_id]['raw']
                    virtual_inventory[mat_id]['raw'] = 0.0
                    virtual_inventory[mat_id]['leftover'] -= rem
                    
                virtual_inventory[mat_id]['total'] -= needed_qty
                
        self.inventory = virtual_inventory
        print(f"Loaded FIFO inventory. {len(self.active_orders)} active orders processed.")

    def check_material_gate(self, product_id, qty):
        """Checks if there's enough virtual inventory for the new order."""
        reqs = self.smeta_reqs.get(product_id, [])
        missing = []
        for r in reqs:
            mat_id = r['mat_id']
            needed_qty = r['qty_per_unit'] * qty
            
            avail_dict = self.inventory.get(mat_id, {'raw': 0.0, 'leftover': 0.0, 'total': 0.0})
            avail_qty = avail_dict.get('total', 0.0)
            avail_raw = avail_dict.get('raw', 0.0)
            avail_leftover = avail_dict.get('leftover', 0.0)
            
            # Avoid showing negative availability (since backlog can push it negative)
            avail_qty = max(0.0, avail_qty)
            avail_raw = max(0.0, avail_raw)
            avail_leftover = max(0.0, avail_leftover)
            
            if avail_raw < needed_qty:
                missing.append({
                    'mat_name': r['mat_name'],
                    'needed_qty': needed_qty,
                    'missing_qty': needed_qty - avail_raw,
                    'avail_raw': avail_raw,
                    'avail_leftover': avail_leftover
                })
        return missing

    def fetch_categorized_operations(self, product_id):
        product_id = str(product_id)
        if product_id in self._ops_cache:
            return self._ops_cache[product_id]
            
        operations = {
            'phase1_prep': [],
            'phase2_assembly': [],
            'phase3_finishing': []
        }
        
        # Phase 1: 36, 39, 40, 41, 42, 43, 44, 51
        # Phase 2: 47
        # Phase 3: 37, 45, 46, 52, 56
        q_ops = f"""
        SELECT gx.xidmet as op_id, gl.name as op_name, gx.miqdar as norm, gx.qiymet as price, gl.qrup
        FROM sm_good_xidmet gx
        JOIN sm_gel gl ON gx.xidmet = gl.idn
        WHERE gx.es_no = {product_id}
        """
        ops = query(q_ops)
        
        # Deduplicate operations by ID just in case sm_good_xidmet has duplicate rows
        seen_ops = set()
        
        for op in ops:
            if op['op_id'] in seen_ops:
                continue
            seen_ops.add(op['op_id'])
            
            qrup = op['qrup']
            op_data = {
                'op_name': op['op_name'],
                'op_id': op['op_id'],
                'norm': float(op['norm']) if op['norm'] else 0.0,
                'price': float(op['price']) if op['price'] else 0.0
            }
            
            if qrup in [36, 39, 40, 41, 42, 43, 44, 51]:
                operations['phase1_prep'].append(op_data)
            elif qrup in [47]:
                operations['phase2_assembly'].append(op_data)
            elif qrup in [37, 45, 46, 52, 56]:
                operations['phase3_finishing'].append(op_data)
            else:
                # Default unknown groups to Assembly
                operations['phase2_assembly'].append(op_data)
        
        self._ops_cache[product_id] = operations
        return operations

    def build_calendar_state(self):
        """Simulates all backlog line items silently to initialize worker calendars."""
        print("Building calendar state from backlog...")
        for o in self.active_orders:
            self.simulate_product(str(o.product_id), o.qty, sourcing_days=0, is_backlog=True)

    def _schedule_phase(self, phase_name, phase_ops, qty, start_dt, assignments):
        import datetime
        if not phase_ops:
            return start_dt
            
        phase_end_dt = start_dt
        
        for op in phase_ops:
            op_id = op['op_id']
            remaining = float(qty)
            
            # Find capable workers for this op
            capable_workers = [w for w in self.workers.values() if op_id in w.capacities]
            
            if not capable_workers:
                # Fallback: assume department can do 50 per day (which is 1 piece every 9.6 minutes)
                minutes_required = (remaining / 50.0) * 480
                op_end_dt = add_working_minutes(start_dt, minutes_required)
                
                assignments.append({
                    "start": start_dt.strftime("%Y-%m-%d %H:%M"),
                    "end": op_end_dt.strftime("%Y-%m-%d %H:%M"),
                    "type": "Department",
                    "phase": phase_name,
                    "op_name": op['op_name'],
                    "name": "Fallback (No Workers)",
                    "qty": round(remaining, 2)
                })
                if op_end_dt > phase_end_dt:
                    phase_end_dt = op_end_dt
                continue
                
            # Distribute work to earliest available capable workers
            while remaining > 0:
                # Get the earliest available worker (but they cannot start before start_dt)
                earliest_worker = min(capable_workers, key=lambda w: max(w.available_from, start_dt))
                worker_start = max(earliest_worker.available_from, start_dt)
                
                # Daily capacity in pieces
                daily_cap = earliest_worker.capacities[op_id]
                if daily_cap <= 0: daily_cap = 1 # safeguard
                
                # Assign up to 10 days of work to a single worker in one chunk if needed to avoid thousands of small entries
                # But to keep it simple, we just assign all remaining to this worker!
                # If they take 100 days, so be it, it's a single block!
                assign_amt = remaining
                
                minutes_required = (assign_amt / daily_cap) * 480
                
                worker_end = add_working_minutes(worker_start, minutes_required)
                
                assignments.append({
                    "start": worker_start.strftime("%Y-%m-%d %H:%M"),
                    "end": worker_end.strftime("%Y-%m-%d %H:%M"),
                    "type": "Worker",
                    "phase": phase_name,
                    "op_name": op['op_name'],
                    "name": earliest_worker.name,
                    "qty": round(assign_amt, 2)
                })
                
                earliest_worker.available_from = worker_end
                remaining = 0 # they took it all in a continuous block
                
                if worker_end > phase_end_dt:
                    phase_end_dt = worker_end
                    
        return phase_end_dt

    def simulate_product(self, product_id, qty, target_deadline=None, sourcing_days=0, worker_cap=50, is_backlog=False):
        """
        Simulates scheduling a single product sequentially with hourly precision.
        """
        import datetime

        # 1. Material Gate Check
        missing_materials = self.check_material_gate(product_id, qty)
        if missing_materials and sourcing_days == 0 and not is_backlog:
            return {
                "status": "WAITING_SOURCING",
                "missing_materials": missing_materials,
                "missing_smeta_orders": self.missing_smeta_orders,
                "message": "Insufficient stock. Please provide Sourcing Time (days)."
            }

        # Determine true start date (09:00 on the calculated day)
        now = datetime.datetime.now()
        start_dt = datetime.datetime(now.year, now.month, now.day, 9, 0) + datetime.timedelta(days=sourcing_days)
        assignments = []
        
        # Cutting Phase (Department Aggregate)
        # Cutting capacity: 200 per day (480 minutes)
        cutting_qty = float(qty)
        minutes_cutting = (cutting_qty / 200.0) * 480
        cutting_end_dt = add_working_minutes(start_dt, minutes_cutting)
        
        assignments.append({
            "start": start_dt.strftime("%Y-%m-%d %H:%M"),
            "end": cutting_end_dt.strftime("%Y-%m-%d %H:%M"),
            "type": "Department",
            "phase": "Cutting",
            "op_name": "Kəsim",
            "name": "Kəsim Şöbəsi",
            "qty": round(cutting_qty, 2)
        })

        # Sewing Phases
        operations_by_phase = self.fetch_categorized_operations(product_id)
        
        # Phase 1: Prep
        phase1_start = cutting_end_dt
        phase1_end = self._schedule_phase("Phase 1 (Prep)", operations_by_phase['phase1_prep'], qty, phase1_start, assignments)
        
        # Phase 2: Assembly
        phase2_start = phase1_end
        phase2_end = self._schedule_phase("Phase 2 (Assembly)", operations_by_phase['phase2_assembly'], qty, phase2_start, assignments)
        
        # Phase 3: Finishing
        phase3_start = phase2_end
        phase3_end = self._schedule_phase("Phase 3 (Finishing)", operations_by_phase['phase3_finishing'], qty, phase3_start, assignments)

        final_delivery_date = phase3_end

        # Deduct from inventory since it's now officially "planned"
        reqs = self.smeta_reqs.get(str(product_id), [])
        for r in reqs:
            if r['mat_id'] in self.inventory:
                self.inventory[r['mat_id']]['total'] -= (r['qty_per_unit'] * qty)

        if is_backlog:
            return

        return {
            "status": "SUCCESS",
            "start_date": start_dt.strftime("%Y-%m-%d %H:%M"),
            "cutting_end_date": cutting_end_dt.strftime("%Y-%m-%d %H:%M"),
            "phase1_start_date": phase1_start.strftime("%Y-%m-%d %H:%M"),
            "phase2_start_date": phase2_start.strftime("%Y-%m-%d %H:%M"),
            "phase3_start_date": phase3_start.strftime("%Y-%m-%d %H:%M"),
            "final_delivery_date": final_delivery_date.strftime("%Y-%m-%d %H:%M"),
            "total_days_required": (final_delivery_date - start_dt).days,
            "missing_smeta_orders": getattr(self, 'missing_smeta_orders', []),
            "operations": operations_by_phase,
            "metrics": {
                "total_assignments": len(assignments)
            },
            "assignments": assignments
        }

    def simulate_order(self, order_id, qty, target_deadline=None, sourcing_days=0, worker_cap=50, is_backlog=False):
        """
        Simulates an entire order by wrapping simulate_product for all its line items.
        """
        import datetime
        products = [o for o in self.active_orders if str(o.order_id) == str(order_id)]
        
        if not products:
            # It's a new ad-hoc product simulation
            return self.simulate_product(str(order_id), qty, target_deadline, sourcing_days, worker_cap, is_backlog)
            
        all_results = []
        for p in products:
            res = self.simulate_product(p.product_id, p.qty, target_deadline, sourcing_days, worker_cap, is_backlog)
            if res:
                all_results.append(res)
                
        if is_backlog: return
        
        # Merge results for frontend display
        merged_assignments = []
        max_delivery = None
        min_start = None
        
        for res in all_results:
            if res.get('status') == 'SUCCESS':
                merged_assignments.extend(res['assignments'])
                end_dt = datetime.datetime.strptime(res['final_delivery_date'], "%Y-%m-%d %H:%M")
                start_dt = datetime.datetime.strptime(res['start_date'], "%Y-%m-%d %H:%M")
                if not max_delivery or end_dt > max_delivery: max_delivery = end_dt
                if not min_start or start_dt < min_start: min_start = start_dt
                
        if not merged_assignments:
            return all_results[0] if all_results else {"status": "ERROR", "message": "No valid products found to simulate."}
            
        return {
            "status": "SUCCESS",
            "start_date": min_start.strftime("%Y-%m-%d %H:%M") if min_start else "",
            "cutting_end_date": max_delivery.strftime("%Y-%m-%d %H:%M"), # Simplification
            "phase1_start_date": max_delivery.strftime("%Y-%m-%d %H:%M"),
            "phase2_start_date": max_delivery.strftime("%Y-%m-%d %H:%M"),
            "phase3_start_date": max_delivery.strftime("%Y-%m-%d %H:%M"),
            "final_delivery_date": max_delivery.strftime("%Y-%m-%d %H:%M") if max_delivery else "",
            "total_days_required": (max_delivery - min_start).days if max_delivery and min_start else 0,
            "missing_smeta_orders": getattr(self, 'missing_smeta_orders', []),
            "operations": {}, # Skip for aggregated
            "metrics": {
                "total_assignments": len(merged_assignments)
            },
            "assignments": merged_assignments
        }

if __name__ == '__main__':
    engine = PlanningEngine()
    engine.load_workers()
    engine.load_inventory_and_backlog()
    print("\n--- Running Simulation ---")
    
    # Try to schedule a dummy order
    dummy_product_id = "1"
    if engine.smeta_reqs:
        # Pick the first product ID that has requirements
        dummy_product_id = list(engine.smeta_reqs.keys())[0]
        
    print(f"Simulating order for product {dummy_product_id}, qty=5000")
    result = engine.simulate_order(order_id=dummy_product_id, qty=5000, sourcing_days=0)
    print("Result (sourcing_days=0):", result)
