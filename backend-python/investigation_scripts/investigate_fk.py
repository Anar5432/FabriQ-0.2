import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('c:/Users/User/.gemini/antigravity/scratch/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import query

sql = """
SELECT 
    fk.name AS FK_name,
    tp.name AS Parent_table,
    cp.name AS Parent_column,
    tr.name AS Referenced_table,
    cr.name AS Referenced_column
FROM sys.foreign_keys fk
INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
INNER JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
INNER JOIN sys.columns cp ON fkc.parent_column_id = cp.column_id AND fkc.parent_object_id = cp.object_id
INNER JOIN sys.columns cr ON fkc.referenced_column_id = cr.column_id AND fkc.referenced_object_id = cr.object_id
WHERE tp.name = 'sm_kontra' AND cp.name = 'emp'
"""
res = query(sql)
print("Foreign keys on sm_kontra.emp:")
print(res)

sql2 = "SELECT TOP 5 * FROM sm_emp"
try:
    print("sm_emp:", query(sql2))
except Exception as e:
    pass

sql3 = "SELECT TOP 5 * FROM users_oper"
try:
    print("users_oper:", query(sql3))
except Exception as e:
    pass
