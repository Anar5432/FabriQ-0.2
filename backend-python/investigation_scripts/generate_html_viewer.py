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

# Get row counts
cursor.execute('''
    SELECT t.name, SUM(p.rows) as rcount
    FROM sys.tables t
    JOIN sys.partitions p ON t.object_id = p.object_id
    WHERE t.is_ms_shipped = 0 AND p.index_id IN (0,1)
    GROUP BY t.name
''')
table_rows = {r.name: r.rcount for r in cursor.fetchall()}

# Get foreign keys
cursor.execute('''
    SELECT tp.name 'Parent', tr.name 'Child'
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables tp ON fk.referenced_object_id = tp.object_id
    INNER JOIN sys.tables tr ON fk.parent_object_id = tr.object_id
''')
fks_raw = set()
for r in cursor.fetchall():
    fks_raw.add((r.Parent, r.Child))

all_tables = set(table_rows.keys())
children = {t: set() for t in all_tables}
parents = {t: set() for t in all_tables}

for p, c in fks_raw:
    if p in all_tables and c in all_tables:
        children[p].add(c)
        parents[c].add(p)

roots = [t for t in all_tables if len(parents[t]) == 0 and len(children[t]) > 0]
roots.sort(key=lambda t: len(children[t]), reverse=True)

green_tables = {
    'sm_kontr_sat', 'sm_kontr_sat_el', 'sm_goods', 'sm_process_iz', 
    'sm_process_iz_el', 'sm_sob_trans_el', 'sm_kontr', 'sm_sob_trans',
    'hm_goods', 'hm_kontr'
}

def get_color_class(t):
    if t in green_tables:
        return 'green'
    elif table_rows.get(t, 0) == 0:
        return 'red'
    else:
        return 'blue'

# We'll explicitly pick 4-5 major roots (trees) to display to avoid overwhelming the browser
target_roots = ['sm_kontr_sat', 'sm_goods', 'sm_process_iz', 'sm_kontr', 'sm_smeta']

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Database Trees Viewer</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true, maxTextSize: 90000, theme: 'default'});</script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; background: #eef2f5; margin: 0; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
        .tree-container { background: white; margin-bottom: 40px; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow-x: auto;}
        h2 { color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; margin-top: 0;}
        .legend { position: sticky; top: 0; background: rgba(255, 255, 255, 0.95); padding: 15px; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-radius: 8px; margin-bottom: 20px; border: 1px solid #ddd; backdrop-filter: blur(5px);}
        .legend-item { display: inline-block; margin-right: 30px; font-weight: bold; color: #333; font-size: 14px;}
        .dot { display: inline-block; width: 16px; height: 16px; border-radius: 50%; margin-right: 8px; vertical-align: text-bottom; }
        .green-dot { background: #d4edda; border: 2px solid #28a745; }
        .blue-dot { background: #cce5ff; border: 2px solid #007bff; }
        .red-dot { background: #f8d7da; border: 2px solid #dc3545; }
        .mermaid { text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin: 0;">Database Tree Viewer (3 Layers Deep)</h1>
        <p style="margin: 10px 0 0 0;">This tool maps out your major database trunks and their child branches, fully separated from each other.</p>
    </div>
    
    <div class="legend">
        <div class="legend-item"><span class="dot green-dot"></span>GREEN: Actively used by our Dashboard program right now</div>
        <div class="legend-item"><span class="dot blue-dot"></span>BLUE: Actively used by the factory (has data), but not in Dashboard</div>
        <div class="legend-item"><span class="dot red-dot"></span>RED: Old / Unused (Zero data inside)</div>
    </div>
"""

for root in target_roots:
    if root not in all_tables:
        continue
        
    html += f'    <div class="tree-container">\n'
    html += f'        <h2>🌲 Tree Trunk: {root}</h2>\n'
    html += f'        <div class="mermaid">\n'
    html += f'            graph TD\n'
    html += f'            classDef green fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;\n'
    html += f'            classDef blue fill:#cce5ff,stroke:#007bff,stroke-width:2px,color:#004085;\n'
    html += f'            classDef red fill:#f8d7da,stroke:#dc3545,stroke-width:2px,color:#721c24;\n'
    
    nodes_to_draw = set()
    edges_to_draw = []
    
    # 3-level extraction
    nodes_to_draw.add(root)
    # L1
    for c1 in children[root]:
        nodes_to_draw.add(c1)
        edges_to_draw.append((root, c1))
        # L2
        for c2 in children[c1]:
            nodes_to_draw.add(c2)
            edges_to_draw.append((c1, c2))
            
    for n in nodes_to_draw:
        c_class = get_color_class(n)
        # Use HTML-safe node names just in case
        html += f'            {n}:::{c_class}\n'
        
    for p, c in edges_to_draw:
        html += f'            {p} --> {c}\n'
        
    html += f'        </div>\n'
    html += f'    </div>\n'

html += """
</body>
</html>
"""

out_path = 'C:/Users/User/.gemini/antigravity/scratch/backend/Database_Trees_Viewer.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
    
print("HTML Viewer Generated!")
