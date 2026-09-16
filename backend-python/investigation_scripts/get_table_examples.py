import os, sys, django, datetime
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.erp_connector import query

CATEGORIES = {
    "Order Details": ["sm_sifaris_form", "sm_sifaris_form_el"],
    "Materials Side of Orders (Smeta / Requirements)": ["sm_smeta", "sm_smeta_xammal", "sm_smeta_satis"],
    "Stock Level & Warehouse Details": ["sm_mal_hes", "sm_sened", "sm_telebname_anbar", "sm_mal_sil"]
}

def get_table_info():
    out = []
    out.append("# Database Tables Overview\\n")
    
    for cat_name, tables in CATEGORIES.items():
        out.append(f"## {cat_name}")
        for table in tables:
            out.append(f"### Table: `{table}`")
            try:
                # Get columns
                cols_data = query(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
                if not cols_data:
                    out.append("*Table not found in database.*\\n")
                    continue
                
                cols = [c['COLUMN_NAME'] for c in cols_data]
                
                # Check for date columns for 'last updated'
                date_cols = [c for c in cols if 'tarix' in c.lower() or 'date' in c.lower() or 'zaman' in c.lower()]
                order_col = date_cols[0] if date_cols else cols[0]
                
                # Get last updated date
                last_updated = "Unknown"
                if date_cols:
                    try:
                        date_res = query(f"SELECT MAX({date_cols[0]}) as last_dt FROM {table}")
                        if date_res and date_res[0]['last_dt']:
                            last_updated = str(date_res[0]['last_dt'])
                    except:
                        pass
                else:
                    # Fallback to getting top 1 and looking at date cols if any
                    pass
                    
                out.append(f"**Last Updated / Inserted:** {last_updated}\\n")
                
                # Get 2 rows
                try:
                    rows = query(f"SELECT TOP 2 * FROM {table} ORDER BY {order_col} DESC")
                except:
                    rows = query(f"SELECT TOP 2 * FROM {table}")
                    
                if not rows:
                    out.append("*No data in table.*\\n")
                    continue
                    
                # Format as markdown table
                # Ensure we only pick up to 8 important columns to fit neatly
                show_cols = cols[:8] 
                
                header = "| " + " | ".join(show_cols) + " |"
                sep = "|" + "|".join(["---"] * len(show_cols)) + "|"
                out.append(header)
                out.append(sep)
                
                for row in rows:
                    row_vals = []
                    for c in show_cols:
                        val = str(row.get(c, ''))
                        # truncate if too long
                        if len(val) > 40: val = val[:37] + "..."
                        val = val.replace('|', '\\|').replace('\\n', ' ')
                        row_vals.append(val)
                    out.append("| " + " | ".join(row_vals) + " |")
                out.append("\\n")
                
            except Exception as e:
                out.append(f"*Error querying table: {e}*\\n")
                
    with open("table_examples_output.md", "w", encoding="utf-8") as f:
        f.write("\\n".join(out))
    print("Done")

if __name__ == '__main__':
    get_table_info()
