import pyodbc
from dashboard.erp_connector import get_connection

def generate_report():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    report_path = r"C:\Users\User\.gemini\antigravity\brain\f7dc54b6-aa30-43e6-b28d-246c5073e231\warehouse_materials_report_2026.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Real-Time Warehouse & Materials Data (2026)\n\n")
        f.write("This report shows the current, active production data from the new ERP modules used in 2026.\n\n")
        
        # 1. sm_sob_trans (Transfers)
        f.write("## 1. Department Transfers (`sm_sob_trans`)\n\n")
        f.write("This tracks the physical movement of items between departments (e.g., from Warehouse to Cutting).\n\n")
        
        try:
            # Let's see what columns we have in sm_sob_trans by selecting a few rows
            cursor.execute("SELECT TOP 5 sen_no, tarix, ins_date, sobe1, sobe2, mebleg, ins_user FROM sm_sob_trans ORDER BY idn DESC")
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            f.write("| " + " | ".join(columns) + " |\n")
            f.write("|" + "|".join(["---"] * len(columns)) + "|\n")
            for row in rows:
                date_str = str(row.tarix)[:10] if row.tarix else '-'
                ins_str = str(row.ins_date)[:16] if row.ins_date else '-'
                f.write(f"| {row.sen_no} | {date_str} | {ins_str} | {row.sobe1} | {row.sobe2} | {row.mebleg} | {row.ins_user} |\n")
        except Exception as e:
            f.write(f"Error querying sm_sob_trans: {e}\n")
            
        f.write("\n---\n")

        # 2. sm_good_ist (Production/Usage)
        f.write("## 2. Production & Material Usage (`sm_good_ist`)\n\n")
        f.write("This table logs the raw materials consumed and products created during production.\n\n")
        
        try:
            # Check what columns exist.
            cursor.execute("SELECT TOP 5 idn, tarix, ins_date, anbar1, anbar2, mebleg, ins_user FROM sm_good_ist ORDER BY idn DESC")
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            f.write("| " + " | ".join(columns) + " |\n")
            f.write("|" + "|".join(["---"] * len(columns)) + "|\n")
            for row in rows:
                date_str = str(row.tarix)[:10] if row.tarix else '-'
                ins_str = str(row.ins_date)[:16] if row.ins_date else '-'
                f.write(f"| {row.idn} | {date_str} | {ins_str} | {row.anbar1} | {row.anbar2} | {row.mebleg} | {row.ins_user} |\n")
        except Exception as e:
            f.write(f"Error querying sm_good_ist: {e}\n")

        f.write("\n---\n")
        
        # 3. What materials are sent?
        # We need the element tables for sm_sob_trans and sm_good_ist
        f.write("## 3. Material Details for Transfers (`sm_sob_trans_el`)\n\n")
        f.write("This table lists the specific raw materials sent during the department transfers.\n\n")
        
        try:
            # Let's try sm_sob_trans_el
            cursor.execute("SELECT TOP 5 es_no, kod, mal, miqdar, sobe FROM sm_sob_trans_el ORDER BY idn DESC")
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            f.write("| " + " | ".join(columns) + " |\n")
            f.write("|" + "|".join(["---"] * len(columns)) + "|\n")
            for row in rows:
                f.write(f"| {row.es_no} | {row.kod} | {row.mal} | {row.miqdar} | {row.sobe} |\n")
        except Exception as e:
            f.write(f"Error querying sm_sob_trans_el: {e}\n")

    conn.close()
    print("Report generated successfully.")

if __name__ == "__main__":
    generate_report()
