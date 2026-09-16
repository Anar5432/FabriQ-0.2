from dashboard.erp_connector import query
import json
orders = query('''
SELECT t.sen_no, t.serh AS company, g.name AS product, tel.miqdar, tel.qaliq, t.tip, tel.mal_tip FROM sm_sifaris t JOIN sm_sifaris_el tel ON t.idn = tel.es_no JOIN sm_goods g ON tel.mal = g.idn WHERE g.name LIKE '%BOZ R-46%' OR g.name LIKE '%ÖNLÜK AĞ İKİ%'
''')
print('ORDERS FOUND:', len(orders))
for row in orders:
    print(json.dumps({k: str(v) for k, v in row.items()}))
