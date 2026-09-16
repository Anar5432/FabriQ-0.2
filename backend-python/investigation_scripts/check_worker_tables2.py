import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django; django.setup()
from dashboard.erp_connector import query

# Get all columns in sm_sobeler_sif
sql = """
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'sm_sobeler_sif'
ORDER BY ORDINAL_POSITION
"""
rows = query(sql)
print("Columns in sm_sobeler_sif:")
for r in rows:
    print(f"  {r['COLUMN_NAME']} ({r['DATA_TYPE']})")

# Get all columns in sm_sobeler_med
sql2 = """
SELECT COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'sm_sobeler_med'
ORDER BY ORDINAL_POSITION
"""
rows2 = query(sql2)
print("\nColumns in sm_sobeler_med:")
for r in rows2:
    print(f"  {r['COLUMN_NAME']} ({r['DATA_TYPE']})")

# Get sample data sm_sobeler_med with correct columns
cols = [r['COLUMN_NAME'] for r in rows2]
cols_str = ', '.join(cols[:8])
sql3 = f"SELECT TOP 5 {cols_str} FROM sm_sobeler_med ORDER BY idn DESC"
rows3 = query(sql3)
print("\nSample data from sm_sobeler_med:")
for row in rows3:
    print(row)

# Also check sm_maya_hes to understand what es_no refers to in sm_maya_gun
sql4 = """
SELECT TOP 5 idn, sen_no, tarix, muddet 
FROM sm_maya_hes 
WHERE muddet IS NOT NULL AND muddet > 0
ORDER BY tarix DESC
"""
rows4 = query(sql4)
print("\nSample from sm_maya_hes with muddet:")
for r in rows4:
    print(r)
