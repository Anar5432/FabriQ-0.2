import os, sys
sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
import django
django.setup()
from dashboard.queries import query

tables = ['sm_rasenka_emp', 'sm_rasenka_emp_el', 'sm_rasenka_emp_el_el', 'sm_emp']
for t in tables:
    cols = query(f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{t}')")
    print(f"{t}:", [c['name'] for c in cols])
