import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

print("--- Checking sm_sifaris_form for idn = 19339 ---")
for row in query("SELECT idn, sen_no, tarix FROM sm_sifaris_form WHERE idn = 19339"):
    print(row)

print("\n--- Checking sm_sif_sened for idn = 19339 ---")
for row in query("SELECT idn, sen_no, tarix FROM sm_sif_sened WHERE idn = 19339"):
    print(row)
