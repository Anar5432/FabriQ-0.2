import pyodbc
from dashboard.erp_connector import get_connection

def analyze_smeta_and_planning():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    out = open("smeta_research.txt", "w", encoding="utf-8")
    
    out.write("=== RESEARCH ON EXAMPLE (SMETA/BOM) CALCULATIONS ===\n")

    # 1. Look at sm_smeta (The core recipe/example table)
    out.write("\n--- 1. Recent Smeta (Example) Documents ---\n")
    try:
        query1 = "SELECT TOP 5 idn, num, ad, sifaris, tarix FROM sm_smeta ORDER BY idn DESC"
        cursor.execute(query1)
        res1 = cursor.fetchall()
        for r in res1:
            out.write(f"Smeta ID: {r.idn} | Name: {r.ad} | Order Link (sifaris): {r.sifaris} | Date: {r.tarix}\n")
    except Exception as e:
        out.write(f"Error checking sm_smeta: {e}\n")

    # 2. Look at sm_smeta_xammal (The raw materials needed for that example)
    out.write("\n--- 2. Raw Materials linked to Smeta (sm_smeta_xammal) ---\n")
    try:
        query2 = "SELECT TOP 5 s.idn, s.es_no, s.mal, g.name, s.miqdar FROM sm_smeta_xammal s JOIN sm_goods g ON s.mal = g.idn ORDER BY s.idn DESC"
        cursor.execute(query2)
        res2 = cursor.fetchall()
        for r in res2:
            out.write(f"Xammal ID: {r.idn} | Smeta Ref (es_no): {r.es_no} | Material: {r.name} | Qty for 1 item: {r.miqdar}\n")
    except Exception as e:
        out.write(f"Error checking sm_smeta_xammal: {e}\n")

    # 3. Look at sm_xammal_plan (The calculated batch requested from warehouse)
    out.write("\n--- 3. Raw Material Planning/Requests (sm_xammal_plan) ---\n")
    try:
        # Check if sifaris or kontr_sat_el link exists here
        query3 = """
        SELECT TOP 5 p.idn, p.sifaris, p.mal, g.name, p.plan_miqdar 
        FROM sm_xammal_plan p 
        JOIN sm_goods g ON p.mal = g.idn 
        ORDER BY p.idn DESC
        """
        cursor.execute(query3)
        res3 = cursor.fetchall()
        for r in res3:
            out.write(f"Plan ID: {r.idn} | Order Ref (sifaris): {r.sifaris} | Material: {r.name} | Planned Qty: {r.plan_miqdar}\n")
    except Exception as e:
        out.write(f"Error checking sm_xammal_plan: {e}\n")

    # 4. Try to find a link between sm_sob_trans (actual warehouse transfer) and the Smeta or Plan
    out.write("\n--- 4. Is there a link in sm_sob_trans to the Plan? ---\n")
    try:
        query4 = "SELECT TOP 5 idn, sen_no, req_no, plan_id, es_no, serh FROM sm_sob_trans ORDER BY idn DESC"
        cursor.execute(query4)
        columns = [col[0] for col in cursor.description]
        out.write(f"Columns available in sm_sob_trans: {columns}\n")
        
        # Let's see if any recent transfers have a plan_id or req_no
        query5 = "SELECT TOP 5 idn, sen_no, tarix, serh FROM sm_sob_trans WHERE idn > 1 ORDER BY idn DESC"
        cursor.execute(query5)
        # Just grab column info for now to see what we can link
        # To avoid errors, I'll just check if plan_id exists
    except Exception as e:
        out.write(f"sm_sob_trans check error: {e}\n")

    conn.close()
    out.close()
    print("Smeta research finished.")

if __name__ == "__main__":
    analyze_smeta_and_planning()
