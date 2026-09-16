import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

# Find all YM lines in sm_sifaris_form (the only table with 'sifaris' column)
sql = """
SELECT 
    e.idn as el_id,
    s.idn as order_id,
    s.sifaris as parent_id,
    g.name
FROM sm_sifaris_form s WITH (NOLOCK)
JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE (g.class IN (18, 20) OR g.name LIKE 'HM-%' OR g.name LIKE 'TM-%')
  AND g.name LIKE '%YM%'
  AND s.tarix >= DATEADD(YEAR, -2, GETDATE())
"""
ym_lines = query(sql)

total_ym = len(ym_lines)
has_parent = [y for y in ym_lines if y['parent_id']]
no_parent = [y for y in ym_lines if not y['parent_id']]

print(f"Total YM lines found (last 2 years): {total_ym}")
print(f"YMs with a parent ID (sifaris): {len(has_parent)}")
print(f"YMs WITHOUT a parent ID: {len(no_parent)}")

if no_parent:
    print("\nExamples of YMs without parent:")
    for y in no_parent[:5]:
        print(f"  Order ID: {y['order_id']}, Product: {y['name']}")

# For those with parent, let's see if the parent exists in kontr_sat or sifaris_form
missing_parents = []
parent_ids = tuple(set([y['parent_id'] for y in has_parent]))

if parent_ids:
    # Check kontr_sat
    sql_k = f"SELECT idn FROM sm_kontr_sat WHERE idn IN {parent_ids}"
    k_parents = {row['idn'] for row in query(sql_k)}
    
    # Check sifaris_form
    sql_f = f"SELECT idn FROM sm_sifaris_form WHERE idn IN {parent_ids}"
    f_parents = {row['idn'] for row in query(sql_f)}
    
    # Check sif_sened
    sql_s = f"SELECT idn FROM sm_sif_sened WHERE idn IN {parent_ids}"
    s_parents = {row['idn'] for row in query(sql_s)}
    
    all_found_parents = k_parents | f_parents | s_parents
    
    for y in has_parent:
        if y['parent_id'] not in all_found_parents:
            missing_parents.append(y)

print(f"\nYMs with a missing parent in the database: {len(missing_parents)}")
if missing_parents:
    print("Examples:")
    for m in missing_parents[:5]:
        print(m)
