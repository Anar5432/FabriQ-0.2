import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
import pyodbc
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
django.setup()

conn_str = f"DRIVER={{{settings.MSSQL_CONFIG['DRIVER']}}};SERVER={settings.MSSQL_CONFIG['SERVER']};DATABASE=BTFERPDB;UID={settings.MSSQL_CONFIG['USERNAME']};PWD={settings.MSSQL_CONFIG['PASSWORD']};TrustServerCertificate=yes;Encrypt=no;"
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

try:
    cursor.execute("SELECT c.name FROM sys.columns c JOIN sys.tables t ON c.object_id = t.object_id WHERE t.name = 'sm_sob_trans'")
    print("sm_sob_trans columns:", [r.name for r in cursor.fetchall()])
    
    # Try finding the primary key table for sobe1 or sobe2 foreign key
    cursor.execute('''
        SELECT tr.name 'Child', c.name 'ChildCol', tp.name 'Parent', cp.name 'ParentCol'
        FROM sys.foreign_keys fk
        INNER JOIN sys.tables tp ON fk.referenced_object_id = tp.object_id
        INNER JOIN sys.tables tr ON fk.parent_object_id = tr.object_id
        INNER JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
        INNER JOIN sys.columns c ON fkc.parent_column_id = c.column_id AND fkc.parent_object_id = c.object_id
        INNER JOIN sys.columns cp ON fkc.referenced_column_id = cp.column_id AND fkc.referenced_object_id = cp.object_id
        WHERE tr.name = 'sm_sob_trans' AND c.name LIKE 'sobe%'
    ''')
    for r in cursor.fetchall():
        print(f"FK: {r.Child}.{r.ChildCol} -> {r.Parent}.{r.ParentCol}")
        
except Exception as e:
    print(e)
