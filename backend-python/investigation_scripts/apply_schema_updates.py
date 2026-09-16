import re

html_files = [
    r'C:\Users\User\.gemini\antigravity\brain\672f7d1e-7d0b-441e-be38-f3f10ade7c45\database_map.html',
    r'C:\Users\User\.gemini\antigravity\brain\672f7d1e-7d0b-441e-be38-f3f10ade7c45\database_map_2d.html'
]

updates = {
    'sm_smeta_xerc': '2026-08',
    'sm_sifaris_form': '2026-07',
    'users_group_oper': '2026-07',
    'sm_tech_plan_cem_xammal': '2026-07',
    'sm_tech_plan_xammal': '2026-07',
    'sm_xm_plan_sif': '2026-07',
    'users_group_report': '2026-07',
    'sm_tech_plan': '2026-06'
}

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for table, date in updates.items():
        # Update 3D map format: Active (Static/Dictionary) -> Active (Last Data: 2026-08) or similar
        # Also need to set has_date: true
        # For 3D Map node objects: {"id": "sm_smeta_xerc", "name": "...", "color": "...", "val": 3, "has_date": false}
        
        # 3D update
        pattern_3d_node = r'(\{"id":\s*"' + table + r'".*?"has_date":\s*)(true|false)(\})'
        content = re.sub(pattern_3d_node, r'\g<1>true\3', content)
        
        pattern_3d_desc = r'(<b>.*? ' + table + r'</b><br/><i>.*?</i><br/>).*?(<br/>Rows: \d+)'
        content = re.sub(pattern_3d_desc, r'\g<1>Active (Last Data: ' + date + r')\g<2>', content)
        
        # 2D update
        pattern_2d_desc = r'(\{"id":\s*"' + table + r'".*?"title":\s*"Rows:\s*\d+\s*\|\s*Updated:\s*)\d{4}-\d{2}-\d{2}(")'
        content = re.sub(pattern_2d_desc, r'\g<1>' + date + r'-01\2', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Successfully applied updates to database schema graphics.")
