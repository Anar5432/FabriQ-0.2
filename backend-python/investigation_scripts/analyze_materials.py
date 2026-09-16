import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()

from dashboard.erp_connector import query

sql_materials = '''
SELECT 
    g.class,
    xammal.mal AS mat_id,
    mat_g.name AS mat_name
FROM sm_goods g WITH (NOLOCK)
JOIN sm_smeta_satis satis WITH (NOLOCK) ON g.idn = satis.mal
JOIN sm_smeta_xammal xammal WITH (NOLOCK) ON satis.es_no = xammal.es_no
JOIN sm_goods mat_g WITH (NOLOCK) ON xammal.mal = mat_g.idn
WHERE g.class IN (18, 20, 21, 29, 30, 22, 24, 27, 31, 32, 34)
'''

rows = query(sql_materials)

category_map = {
    18: 'Underwear', 20: 'Underwear',
    21: 'Corab', 29: 'Corab', 30: 'Corab',
    22: 'Isci', 24: 'Isci', 27: 'Isci', 31: 'Isci', 32: 'Isci', 34: 'Isci'
}

mat_categories = {}
mat_names = {}

for r in rows:
    cat = category_map.get(r['class'])
    if not cat: continue
    mat_id = r['mat_id']
    mat_names[mat_id] = r['mat_name']
    
    if mat_id not in mat_categories:
        mat_categories[mat_id] = set()
    mat_categories[mat_id].add(cat)

underwear_mats = {mid for mid, cats in mat_categories.items() if 'Underwear' in cats}
shared_mats = {mid for mid in underwear_mats if len(mat_categories[mid]) > 1}
exclusive_mats = underwear_mats - shared_mats

print(f'Total materials used in Underwear: {len(underwear_mats)}')
print(f'Materials EXCLUSIVE to Underwear: {len(exclusive_mats)}')
print(f'Materials SHARED with other categories: {len(shared_mats)}')

if shared_mats:
    print('\n--- SHARED MATERIALS ---')
    for mid in shared_mats:
        other_cats = mat_categories[mid] - {'Underwear'}
        cat_str = ", ".join(other_cats)
        print(f'- [{mid}] {mat_names[mid]} (Used by Underwear AND {cat_str})')
