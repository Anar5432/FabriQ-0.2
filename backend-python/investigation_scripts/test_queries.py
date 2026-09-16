import sys
import os
import copy
import re
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dashboard.erp_connector import query

def test_get_orders_hybrid():
    sector = 'isci'
    cls = "(27)"
    
    # Step 1: Base lines
    sql = f"""
    SET NOCOUNT ON;
    SELECT
        s.idn AS order_id,
        s.sen_no,
        CONVERT(VARCHAR(10), s.tarix, 23) AS tarix,
        s.kontra AS company_id,
        s.kontra_name AS company_name,
        e.idn AS line_id,
        e.num AS line_num,
        g.idn AS product_id,
        g.name AS product_name,
        e.miqdar AS qty_ordered,
        e.qaliq AS qty_remaining
    FROM sm_kontr_sat s WITH (NOLOCK)
    JOIN sm_kontr_sat_el e WITH (NOLOCK) ON e.es_no = s.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    WHERE g.class IN {cls}
      AND (e.qaliq > 0 OR s.tarix >= DATEADD(DAY, -60, GETDATE()))
    ORDER BY s.tarix ASC, e.num;
    """
    base_lines = query(sql)
    print(f"Loaded {len(base_lines)} base lines.")

    # Step 2: FIFO Balances
    sql_balances = f"""
    SELECT 
        hm_goods.idn AS hm_mal,
        dept.idn AS dept_id,
        ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) AS balance
    FROM sm_goods hm_goods WITH (NOLOCK)
    JOIN sm_goods ym_g WITH (NOLOCK) ON 
        ym_g.class IN {cls} AND (
            hm_goods.idn = ym_g.idn
            OR (ym_g.name LIKE 'YM-%' AND hm_goods.name LIKE 'HM-%'
                AND SUBSTRING(ym_g.name, 4, LEN(ym_g.name)) = SUBSTRING(hm_goods.name, 4, LEN(hm_goods.name)))
        )
    JOIN (
        SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        WHERE t.tesdiq = 1
        GROUP BY t.sobe2, tel.mal
    ) ins ON ym_g.idn = ins.mal
    LEFT JOIN sm_depo dept WITH (NOLOCK) ON ins.dept_id = dept.idn
    LEFT JOIN (
        SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out
        FROM sm_sob_trans t WITH (NOLOCK)
        JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
        WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL
        GROUP BY t.sobe1, tel.mal
    ) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal
    WHERE hm_goods.class IN {cls}
      AND (ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0)) > 0
    """
    balances_raw = query(sql_balances)
    product_balances = defaultdict(lambda: defaultdict(float))
    for b in balances_raw:
        product_balances[b['hm_mal']][b['dept_id']] += float(b['balance'])

    # Step 2.5: Comments
    sql_comments = """
    SELECT 
        t.sobe2 AS dept_id, 
        t.serh, 
        tel.qeyd
    FROM sm_sob_trans t WITH (NOLOCK)
    JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no
    WHERE t.tesdiq = 1 AND t.tarix >= DATEADD(DAY, -60, GETDATE())
      AND ((t.serh IS NOT NULL AND t.serh != '') OR (tel.qeyd IS NOT NULL AND tel.qeyd != ''))
    GROUP BY t.sobe2, t.serh, tel.qeyd
    """
    comments_raw = query(sql_comments)
    comment_strings = []
    for c in comments_raw:
        text = f"{c['serh'] or ''} {c['qeyd'] or ''}".lower()
        comment_strings.append({
            'dept_id': c['dept_id'],
            'text': text
        })
        
    raw_lines = []
    comment_matches_count = 0
    fifo_matches_count = 0
    
    for order in base_lines:
        qaliq = float(order['qty_remaining'] or 0)
        ordered = float(order['qty_ordered'] or 0)
        delivered = ordered - qaliq
        
        if delivered > 0:
            o_deliv = copy.deepcopy(order)
            o_deliv['qty_remaining'] = 0
            o_deliv['split_display'] = f"{int(delivered)}/{int(ordered)}"
            o_deliv['current_phase'] = 6
            raw_lines.append(o_deliv)
            
        if qaliq == 0:
            continue
            
        # FUZZY MATCH
        cname = (order['company_name'] or '').lower()
        cname_clean = re.sub(r'\b(mmc|baki|azerbaycan|qapali sehmdar cemiyyeti|qsc|mms|llc)\b', '', cname).strip()
        words = cname_clean.split()
        search_key = words[0] if words and len(words[0]) > 3 else (" ".join(words[:2]) if words else "")
        
        matched_dept = None
        if search_key:
            dept_priority = [6, 15, 39, 5, 4, 3, 24, 8, 9]
            matched_depts = set()
            for c in comment_strings:
                # We want whole word match or strong substring
                if search_key in c['text']:
                    matched_depts.add(c['dept_id'])
                    
            for d in dept_priority:
                if d in matched_depts:
                    matched_dept = d
                    break
                    
        if matched_dept is not None:
            o_split = copy.deepcopy(order)
            o_split['qty_remaining'] = qaliq
            o_split['split_display'] = f"{int(qaliq)}/{int(ordered)}"
            o_split['current_phase'] = matched_dept
            o_split['match_type'] = 'comment'
            raw_lines.append(o_split)
            comment_matches_count += 1
            continue
            
        # FIFO MATCH
        hm_mal = order['product_id']
        bals = product_balances[hm_mal]
        dept_priority = [6, 15, 39, 5, 4, 3, 24, 8, 9]
        remaining_to_find = qaliq
        
        for dept_id in dept_priority:
            if remaining_to_find <= 0:
                break
            available = bals[dept_id]
            if available > 0:
                take = min(available, remaining_to_find)
                bals[dept_id] -= take
                remaining_to_find -= take
                
                o_split = copy.deepcopy(order)
                o_split['qty_remaining'] = qaliq
                o_split['split_display'] = f"{int(take)}/{int(ordered)}"
                o_split['current_phase'] = dept_id
                o_split['match_type'] = 'fifo'
                raw_lines.append(o_split)
                fifo_matches_count += 1
                
        if remaining_to_find > 0:
            o_split = copy.deepcopy(order)
            o_split['qty_remaining'] = qaliq
            o_split['split_display'] = f"{int(remaining_to_find)}/{int(ordered)}" if remaining_to_find < ordered else ""
            o_split['current_phase'] = 0
            o_split['match_type'] = 'none'
            raw_lines.append(o_split)
            
    # Output stats
    with open("hybrid_stats.txt", "w", encoding="utf-8") as f:
        f.write(f"Total Base Lines Processed: {len(base_lines)}\n")
        f.write(f"Lines Matched by Comment: {comment_matches_count}\n")
        f.write(f"Lines Matched by FIFO: {fifo_matches_count}\n")
        
        # Breakdown by phase
        f.write("\n--- Phase Breakdown ---\n")
        from collections import Counter
        phases = Counter(r['current_phase'] for r in raw_lines)
        for phase, count in phases.items():
            f.write(f"Phase {phase}: {count} items\n")

if __name__ == "__main__":
    test_get_orders_hybrid()
