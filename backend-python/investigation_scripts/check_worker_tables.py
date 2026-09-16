import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

tables = [
    # Daily production log - has employee count and hours
    ("sm_maya_gun", """
        SELECT TOP 5 idn, tarix, es_no, emp_say, is_saat, saat, deqiqe
        FROM sm_maya_gun
        ORDER BY tarix DESC
    """),
    # The parent record for sm_maya_gun
    ("sm_maya_hes (parent of sm_maya_gun)", """
        SELECT TOP 5 idn, sen_no, tarix, muddet, ins_user
        FROM sm_maya_hes
        ORDER BY tarix DESC
    """),
    # Another candidate - shift/schedule data
    ("sm_sobeler_med (Dept working hours)", """
        SELECT TOP 5 idn, sobe, bas_vaxt, bit_vaxt
        FROM sm_sobeler_med
        ORDER BY idn DESC
    """),
    # Workers assigned to departments
    ("sm_sobeler_sif (Dept orders)", """
        SELECT TOP 5 idn, sobe, mal, miqdar, tech_plan
        FROM sm_sobeler_sif
        ORDER BY idn DESC
    """),
]

for name, sql in tables:
    print(f"\n{'='*60}")
    print(f"TABLE: {name}")
    print('='*60)
    try:
        rows = query(sql)
        if not rows:
            print("  [EMPTY - No data]")
        else:
            for i, row in enumerate(rows):
                print(f"  Row {i+1}:")
                for k, v in row.items():
                    if v is not None and str(v).strip() != '':
                        print(f"    {k}: {v}")
    except Exception as e:
        print(f"  [ERROR: {e}]")
