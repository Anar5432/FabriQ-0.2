import pyodbc
from dashboard.erp_connector import get_connection

def analyze_comments():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    out = open("comment_analysis.txt", "w", encoding="utf-8")
    
    out.write("=== COMMENT ANALYSIS ===\n")
    
    # Let's get the last 50 transfers with any comments
    query = """
    SELECT TOP 50 
        t.sen_no, 
        t.tarix, 
        t.sobe1, 
        t.sobe2,
        t.serh, 
        tel.qeyd,
        s1.name AS from_dept,
        s2.name AS to_dept
    FROM sm_sob_trans t
    JOIN sm_sob_trans_el tel ON t.idn = tel.es_no
    LEFT JOIN sm_depo s1 ON t.sobe1 = s1.idn
    LEFT JOIN sm_depo s2 ON t.sobe2 = s2.idn
    WHERE t.tarix >= '2026-05-01'
      AND ((t.serh IS NOT NULL AND t.serh != '') OR (tel.qeyd IS NOT NULL AND tel.qeyd != ''))
    ORDER BY t.idn DESC
    """
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for r in results:
            serh_text = r.serh.strip() if r.serh else ""
            qeyd_text = r.qeyd.strip() if r.qeyd else ""
            
            # Print if there is a real comment
            if serh_text or qeyd_text:
                out.write(f"Transfer: {r.sen_no} | {r.tarix} | {r.from_dept} -> {r.to_dept}\n")
                if serh_text:
                    out.write(f"  Comment (serh): '{serh_text}'\n")
                if qeyd_text:
                    out.write(f"  Note (qeyd): '{qeyd_text}'\n")
                out.write("-" * 40 + "\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    conn.close()
    out.close()
    print("Comment analysis finished.")

if __name__ == "__main__":
    analyze_comments()
