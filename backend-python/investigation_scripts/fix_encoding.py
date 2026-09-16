import os

# Read the correctly encoded names
with open('worker_list.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = {}
current_pos = None
for line in lines:
    line = line.strip()
    if line.startswith('# '):
        current_pos = line[2:].split(' (')[0].strip()
        if current_pos.lower() == 'tikişçi': current_pos = 'TİKİŞÇİ'
        if current_pos not in data:
            data[current_pos] = []
    elif line.startswith('- '):
        data[current_pos].append(line[2:])

md = "# Worker Detailed Categorization Template\n\n"
md += "Here is the exact breakdown of all active workers in your database, mapped to their missing information details.\n\n"

md += "## Tier 1: Lack Sub-category and Specific Ability Details\n"
md += "These workers have a general category, but we have no data on whether they work in the Front, Middle, or End stages, nor what their specific machine/stitch abilities are.\n\n"

if 'TİKİŞÇİ' in data:
    md += "### Category: Tikiş (Sewing)\n"
    md += "**Detail:** Sub-category (Front/Mid/End) is MISSING. Specific Ability is MISSING.\n\n"
    for w in data['TİKİŞÇİ']: md += f"- {w}\n"
    md += "\n"

toxucu_workers = data.get('Toxucu', []) + data.get('Corab sexi', [])
if toxucu_workers:
    md += "### Category: Toxucu / Corab sexi\n"
    md += "**Detail:** Sub-category is MISSING. Specific Ability is MISSING.\n\n"
    for w in toxucu_workers: md += f"- {w}\n"
    md += "\n"

if 'Araçı' in data:
    md += "### Category: Araçı (Ambiguous)\n"
    md += "**Detail:** Exact Category (Cutting/Sewing) is MISSING. Specific Ability is MISSING.\n\n"
    for w in data['Araçı']: md += f"- {w}\n"
    md += "\n"


md += "## Tier 2: Have Sub-category, but Lack Specific Ability Details\n"
md += "We can guess the sub-category based on their title, but we lack specific technical abilities.\n\n"

md += "### Category: Kəsim (Cutting)\n"
md += "**Detail:** Has Front Stage role (Lekalçı), but missing Specific Ability.\n\n"
front_cut = data.get('Lekalçı', []) + data.get('Lekal operatoru', [])
for w in front_cut: md += f"- {w}\n"
md += "\n"

md += "**Detail:** Has Mid Stage role (Kəsimçi / Beyka kəsən), but missing Specific Ability.\n\n"
mid_cut = data.get('Kəsimçi', []) + data.get('Beyka kəsən', []) + data.get('ön kəsim', [])
for w in mid_cut: md += f"- {w}\n"
md += "\n"

md += "### Category: Tikiş (Sewing)\n"
md += "**Detail:** Has End Stage role (Ütücü / Qablaşdırıcı / Təmizlikçi), but missing Specific Ability.\n\n"
end_sew = data.get('Ütücü', []) + data.get('Qablaşdırıcı', []) + data.get('Tikiş təmizlikçisi', []) + data.get('Etiketçi', []) + data.get('Rosso', [])
for w in end_sew: md += f"- {w}\n"
md += "\n"

md += "**Detail:** Has Mid Stage role (İlgək / Düymə), but missing Specific Ability.\n\n"
mid_sew = data.get('düymə -petlə operatoru', []) + data.get('Petlə düymə maşını üzrə operator', [])
for w in mid_sew: md += f"- {w}\n"
md += "\n"


md += "## Tier 3: Out of Scope / Support Staff\n"
md += "These roles are administrative, logistical, or maintenance, and do not need to be mapped into the Cutting/Sewing production stages.\n\n"

other_keys = [k for k in data.keys() if k not in ['TİKİŞÇİ', 'Toxucu', 'Corab sexi', 'Araçı', 'Lekalçı', 'Lekal operatoru', 'Kəsimçi', 'Beyka kəsən', 'ön kəsim', 'Ütücü', 'Qablaşdırıcı', 'Tikiş təmizlikçisi', 'Etiketçi', 'Rosso', 'düymə -petlə operatoru', 'Petlə düymə maşını üzrə operator', 'Tikişçi', 'tikişçi']]
for k in other_keys:
    md += f"### {k}\n"
    for w in data[k]: md += f"- {w}\n"
    md += "\n"

with open(r'c:\Users\User\.gemini\antigravity\brain\c51a54e5-4176-4992-9ea7-27a27e2593dc\worker_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(md)

