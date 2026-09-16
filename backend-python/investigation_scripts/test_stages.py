import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.queries import query

sql_depts = '''
SELECT TOP 10 d.name as dept_name, count(*) as count 
FROM sm_sob_trans_el tel WITH (NOLOCK)
JOIN sm_sob_trans t WITH (NOLOCK) ON t.idn = tel.es_no
JOIN sm_depo d WITH (NOLOCK) ON t.sobe2 = d.idn
JOIN sm_goods g WITH (NOLOCK) ON tel.mal = g.idn
WHERE g.class IN (21, 29, 30) AND t.tesdiq = 1
GROUP BY d.name
ORDER BY count DESC
'''

sql_faza = '''
SELECT TOP 10 f.name as faza_name, count(*) as count 
FROM sm_good_ist_el e WITH (NOLOCK)
JOIN sm_faza f WITH (NOLOCK) ON e.son_faza = f.idn
JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
WHERE g.class IN (21, 29, 30)
GROUP BY f.name
ORDER BY count DESC
'''

print('Top Departments for Corab (sm_depo via sm_sob_trans):')
res_depts = query(sql_depts)
for r in res_depts:
    name = (r['dept_name'] or '').encode('ascii', 'ignore').decode('ascii')
    print(' - ' + name + ' (' + str(r['count']) + ')')

print('\nTop Phases for Corab (sm_faza via sm_good_ist):')
res_faza = query(sql_faza)
for r in res_faza:
    name = (r['faza_name'] or '').encode('ascii', 'ignore').decode('ascii')
    print(' - ' + name + ' (' + str(r['count']) + ')')
