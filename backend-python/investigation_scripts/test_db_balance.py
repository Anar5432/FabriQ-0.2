from dashboard.erp_connector import query
import json
balances = query('''
SELECT dept.idn AS dept_id, ISNULL(ins.qty_in, 0) - ISNULL(outs.qty_out, 0) AS balance FROM sm_goods ym_g JOIN (SELECT t.sobe2 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_in FROM sm_sob_trans t JOIN sm_sob_trans_el tel ON t.idn = tel.es_no WHERE t.tesdiq = 1 GROUP BY t.sobe2, tel.mal) ins ON ym_g.idn = ins.mal LEFT JOIN sm_depo dept ON ins.dept_id = dept.idn LEFT JOIN (SELECT t.sobe1 AS dept_id, tel.mal, SUM(tel.miqdar) AS qty_out FROM sm_sob_trans t JOIN sm_sob_trans_el tel ON t.idn = tel.es_no WHERE t.tesdiq = 1 AND t.sobe1 IS NOT NULL GROUP BY t.sobe1, tel.mal) outs ON ins.dept_id = outs.dept_id AND ins.mal = outs.mal WHERE ym_g.name LIKE '%BOZ R-46%' OR ym_g.name LIKE '%ÖNLÜK AĞ İKİ%'
''')
for row in balances:
    print(json.dumps({k: str(v) for k, v in row.items()}))
