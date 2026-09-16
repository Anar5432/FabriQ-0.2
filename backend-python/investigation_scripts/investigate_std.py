import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = "SELECT * FROM sm_good_ist WHERE idn = 25650"
print("--- Full record for 25650 ---")
for row in query(sql):
    for k, v in row.items():
        if v is not None and v != '' and v != 0 and v != False:
            print(f"{k}: {repr(v)}")

# See if there is any customer ID in any field
print("\n--- Any matching order in sm_sifaris_form? ---")
sql2 = "SELECT * FROM sm_sifaris_form WHERE sen_no = '025650' OR idn = 25650"
res2 = query(sql2)
if res2:
    print("Found in sm_sifaris_form!")
else:
    print("Not found in sm_sifaris_form.")
