import pyodbc
from dashboard.erp_connector import get_connection

def update_report():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    report_path = r"C:\Users\User\.gemini\antigravity\brain\f7dc54b6-aa30-43e6-b28d-246c5073e231\warehouse_materials_report.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Warehouse & Raw Materials Data Report (With Timelines)\n\n")
        f.write("This updated document includes the timelines (Dates, Creation Time) for the warehouse transactions. I have also added information about other tables containing raw material details.\n\n")
        
        # Other tables explanation
        f.write("## Are there other tables with Raw Material details?\n")
        f.write("Yes! Besides the usage and transfer tables, the database also contains:\n")
        f.write("- **`sm_good_xammal`**: This is the master catalog of all raw materials (names, codes, base prices).\n")
        f.write("- **`sm_xammal_plan` & `sm_xammal_plan_cem`**: These tables are used for Planning and Estimating what raw materials will be needed for future orders before they are actually transferred.\n")
        f.write("- **`sm_smeta_xammal`**: Contains the cost estimates (Smeta) for the raw materials.\n\n")
        f.write("---\n")

        # 1. Latest Raw Material Usage
        f.write("## 1. Latest Raw Material Usage & Transfers (`sm_good_ist_xammal`)\n\n")
        f.write("Since the `sm_good_ist_xammal` table doesn't have a date column itself, it links back to a header document (via `es_no`). I have joined it with the `sm_sifaris_form` / orders to find the exact creation timeline.\n\n")
        f.write("| Usage ID | Material ID | Dept/Stage | Dest. Qty | Qty | Balance | **Timeline (Date)** |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        try:
            # Try to get date from header if possible, or just raw if it fails. Let's join with sm_sifaris_form which has dates
            query = """
            SELECT TOP 10 
                x.idn, x.mal, x.sobe, x.faza, x.tey_miq, x.miqdar, x.qaliq1,
                f.tarix, f.ins_date
            FROM sm_good_ist_xammal x
            LEFT JOIN sm_sifaris_form f ON x.es_no = f.idn
            ORDER BY x.idn DESC
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                # Formatted date
                date_str = str(row.ins_date)[:16] if row.ins_date else (str(row.tarix)[:10] if row.tarix else 'No Date Found')
                f.write(f"| {row.idn} | {row.mal} | {row.sobe} / {row.faza} | {row.tey_miq} | {row.miqdar} | {row.qaliq1} | **{date_str}** |\n")
        except Exception as e:
            f.write(f"Error: {e}\n")
            
        f.write("\n---\n")

        # 2. Latest Waybills
        f.write("## 2. Latest Order Waybills / Material Transfers (`sm_sifaris_qaime`)\n\n")
        f.write("This table has direct timelines for when the transfer document was created and approved.\n\n")
        f.write("| Waybill No | **Creation Date/Time** | **Action Date** | Order No | User |\n")
        f.write("|---|---|---|---|---|\n")
        
        try:
            cursor.execute("SELECT TOP 10 sen_no, ins_date, tarix, sif_no, ins_user FROM sm_sifaris_qaime ORDER BY idn DESC")
            for row in cursor.fetchall():
                action_date = str(row.tarix)[:10] if row.tarix else '-'
                creation_time = str(row.ins_date)[:16] if row.ins_date else '-'
                f.write(f"| {row.sen_no} | **{creation_time}** | {action_date} | {row.sif_no} | {row.ins_user} |\n")
        except Exception as e:
            f.write(f"Error: {e}\n")
            
        f.write("\n---\n")
        
        # 3. Detailed Waybill Elements
        f.write("## 3. Detailed Materials for Waybills (`sm_sifaris_qaime_el_el`)\n\n")
        f.write("We join this details table back to the main Waybill (`sm_sifaris_qaime`) to show the exact timeline for each material line item.\n\n")
        f.write("| Material Code | Material ID | Stage (Faza) | Waybill Ref | **Timeline (Inserted On)** |\n")
        f.write("|---|---|---|---|---|\n")
        
        try:
            query = """
            SELECT TOP 10 
                el.kod, el.mal, el.faza, el.es_no, 
                q.ins_date 
            FROM sm_sifaris_qaime_el_el el
            LEFT JOIN sm_sifaris_qaime q ON el.es_no = q.idn
            ORDER BY el.idn DESC
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                time_str = str(row.ins_date)[:16] if row.ins_date else '-'
                f.write(f"| {row.kod} | {row.mal} | {row.faza} | {row.es_no} | **{time_str}** |\n")
        except Exception as e:
            f.write(f"Error: {e}\n")

    conn.close()
    print("Report updated.")

if __name__ == "__main__":
    update_report()
