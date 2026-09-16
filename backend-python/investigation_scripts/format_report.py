import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

res = query("SELECT p.name as pos, e.name as emp_name FROM sm_emp e LEFT JOIN sm_position p ON e.position = p.idn WHERE e.ise_son IS NULL ORDER BY p.name, e.name")

data = {}
for r in res:
    p = (r['pos'] or 'Bilinmir').strip()
    # normalize names
    if p.lower() == 'tikişçi': p = 'TİKİŞÇİ'
    
    n = r['emp_name'].strip()
    if p not in data: data[p] = []
    data[p].append(n)

md = "# Worker Detailed Categorization Report\n\n"
md += "Here is the exact breakdown of all active workers in your database, matched with the missing information details.\n\n"

md += "## Tier 1: Lack Sub-category and Specific Ability Details\n"
md += "These workers have a general category (Sewing/Knitting), but we have no data on whether they work in the Front, Middle, or End stages, nor what their specific machine/stitch abilities are.\n\n"

if 'TİKİŞÇİ' in data:
    md += "### Category: Tikiş (Sewing)\n"
    md += "**Detail:** Sub-category (Front/Mid/End) is MISSING. Specific Ability is MISSING.\n\n"
    for w in data['TİKİŞÇİ']:
        md += f"- {w}\n"
    md += "\n"

# Corab / Toxucu
toxucu_workers = data.get('Toxucu', []) + data.get('Corab sexi', [])
if toxucu_workers:
    md += "### Category: Toxucu / Corab sexi\n"
    md += "**Detail:** Sub-category is MISSING. Specific Ability is MISSING.\n\n"
    for w in toxucu_workers:
        md += f"- {w}\n"
    md += "\n"

if 'Araçı' in data:
    md += "### Category: Araçı (Ambiguous)\n"
    md += "**Detail:** Exact Category (Cutting/Sewing) is MISSING. Specific Ability is MISSING.\n\n"
    for w in data['Araçı']:
        md += f"- {w}\n"
    md += "\n"


md += "## Tier 2: Have Sub-category, but Lack Specific Ability Details\n"
md += "We can reasonably guess the sub-category based on their title, but we still lack their specific technical abilities (e.g. Laser Cutting vs Manual, Overlock vs Straight Stitch).\n\n"

md += "### Category: Kəsim (Cutting)\n"
md += "**Detail:** Has Front Stage role (Lekalçı), but missing Specific Ability.\n\n"
front_cut = data.get('Lekalçı', []) + data.get('Lekal operatoru', [])
for w in front_cut:
    md += f"- {w}\n"
md += "\n"

md += "**Detail:** Has Mid Stage role (Kəsimçi / Beyka kəsən), but missing Specific Ability.\n\n"
mid_cut = data.get('Kəsimçi', []) + data.get('Beyka kəsən', []) + data.get('ön kəsim', [])
for w in mid_cut:
    md += f"- {w}\n"
md += "\n"

md += "### Category: Tikiş (Sewing)\n"
md += "**Detail:** Has End Stage role (Ütücü / Qablaşdırıcı / Təmizlikçi), but missing Specific Ability.\n\n"
end_sew = data.get('Ütücü', []) + data.get('Qablaşdırıcı', []) + data.get('Tikiş təmizlikçisi', []) + data.get('Etiketçi', []) + data.get('Rosso', [])
for w in end_sew:
    md += f"- {w}\n"
md += "\n"

md += "**Detail:** Has Mid Stage role (İlgək / Düymə), but missing Specific Ability.\n\n"
mid_sew = data.get('düymə -petlə operatoru', []) + data.get('Petlə düymə maşını üzrə operator', [])
for w in mid_sew:
    md += f"- {w}\n"
md += "\n"


md += "## Tier 3: Out of Scope / Support Staff\n"
md += "These roles are administrative, logistical, or maintenance, and do not need to be mapped into the Cutting/Sewing production stages.\n\n"

other_keys = [k for k in data.keys() if k not in ['TİKİŞÇİ', 'Toxucu', 'Corab sexi', 'Araçı', 'Lekalçı', 'Lekal operatoru', 'Kəsimçi', 'Beyka kəsən', 'ön kəsim', 'Ütücü', 'Qablaşdırıcı', 'Tikiş təmizlikçisi', 'Etiketçi', 'Rosso', 'düymə -petlə operatoru', 'Petlə düymə maşını üzrə operator']]
for k in other_keys:
    md += f"### {k}\n"
    for w in data[k]:
        md += f"- {w}\n"
    md += "\n"


with open(r'c:\Users\User\.gemini\antigravity\brain\c51a54e5-4176-4992-9ea7-27a27e2593dc\worker_analysis_report.md', 'w', encoding='utf-8') as f:
    f.write(md)

