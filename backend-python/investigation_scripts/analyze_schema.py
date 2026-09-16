import os
import io
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def analyze():
    out = io.StringIO()
    
    # Get the SMETA ID for HM-MAYKA ALPAR BOZ R-XL (Good ID: 36400)
    good_id = 36400
    smetas = query(f"SELECT es_no FROM sm_smeta_satis WHERE mal = {good_id}")
    if not smetas:
        out.write("No SMETA found for 36400\n")
        return out.getvalue()
        
    smeta_id = smetas[0]['es_no']
    out.write(f"SMETA ID is {smeta_id}\n")
    
    # Check how many products use this SMETA
    products = query(f"SELECT g.name FROM sm_smeta_satis s JOIN sm_goods g ON s.mal = g.idn WHERE s.es_no = {smeta_id}")
    out.write(f"This SMETA is shared by {len(products)} products!\n")
    for p in products[:10]:
        out.write(f"  - {p['name']}\n")
        
    return out.getvalue()

if __name__ == "__main__":
    result = analyze()
    with io.open("analyze_materials_schema.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print("Done")

if __name__ == "__main__":
    result = analyze()
    with io.open("analyze_materials_schema.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print("Done. Wrote to analyze_materials_schema.txt")
