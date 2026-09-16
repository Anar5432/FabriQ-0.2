from dashboard.erp_connector import query
import json
orders = query('''
SELECT t.sen_no, g.name AS product, tel.miqdar, tel.qaliq, t.tarix FROM sm_sifaris t JOIN sm_sifaris_el tel ON t.idn = tel.es_no JOIN sm_goods g ON tel.mal = g.idn WHERE t.sen_no = '022386'
''')
for row in orders:
    print(json.dumps({k: str(v) for k, v in row.items()}))
