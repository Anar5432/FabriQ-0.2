from dashboard.erp_connector import query
import json

res = query("SELECT idn, name, class FROM sm_goods WHERE name = 'HM-BETEX/09/0018 AĞ KÖYNƏK KİŞİ R-2XL' OR name LIKE '%HM-BETEX/09/0018%'")
for row in res:
    print(json.dumps({k: str(v) for k, v in row.items()}))
