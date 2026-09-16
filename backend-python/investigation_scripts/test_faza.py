import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.queries import query

res = query('SELECT idn, name FROM sm_faza WITH (NOLOCK) ORDER BY idn')
for r in res:
    print(str(r['idn']) + ' - ' + str((r['name'] or '').encode('ascii', 'ignore').decode('ascii')))
