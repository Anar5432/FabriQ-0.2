import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

keyword_cond = "(g.name LIKE '%BOXER%' OR g.name LIKE '%KÜLOT%' OR g.name LIKE '%KULOT%' OR g.name LIKE '%MAYKA%' OR g.name LIKE '%BODY%' OR g.name LIKE '%SLİP%' OR g.name LIKE '%SLIP%')"
keyword_prefix = "(g.name LIKE 'HM-%' OR g.name LIKE 'YM-%' OR g.name LIKE 'TM-%')"
class_condition = f"(g.class = 20 OR ({keyword_cond} AND {keyword_prefix}))"

sql = f"""
SELECT COUNT(DISTINCT g.idn) as c
FROM sm_goods g
WHERE {class_condition}
"""
results = query(sql)
print(f"Total matching items for the new Underwear rule: {results[0]['c']}")

# Let's count how many are purely class 20 vs how many are keyword
sql2 = f"""
SELECT 
    SUM(CASE WHEN g.class = 20 THEN 1 ELSE 0 END) as class20_count,
    SUM(CASE WHEN (g.class != 20 OR g.class IS NULL) THEN 1 ELSE 0 END) as keyword_count
FROM sm_goods g
WHERE {class_condition}
"""
results2 = query(sql2)
print(f"Class 20 items: {results2[0]['class20_count']}")
print(f"Keyword matched (miscategorized) items: {results2[0]['keyword_count']}")

