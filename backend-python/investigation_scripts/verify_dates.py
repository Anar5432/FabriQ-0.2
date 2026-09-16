import pyodbc
from dashboard.erp_connector import get_connection

def verify_recent_data():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    
    print("--- Checking Recent Dates in Active Dashboard Tables ---")
    
    queries = {
        "sm_kontr_sat (Sales Orders)": "SELECT TOP 3 tarix, ins_date FROM sm_kontr_sat ORDER BY idn DESC",
        "sm_good_ist (Production/Usage)": "SELECT TOP 3 tarix, ins_date FROM sm_good_ist ORDER BY idn DESC",
        "sm_sob_trans (Transfers)": "SELECT TOP 3 tarix, ins_date FROM sm_sob_trans ORDER BY idn DESC",
        "sm_mal_say (Stock)": "SELECT TOP 3 tarix, ins_date FROM sm_mal_say ORDER BY idn DESC"
    }
    
    for name, query in queries.items():
        print(f"\n{name}")
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                print(f"Date: {row.tarix}, Inserted: {row.ins_date}")
        except Exception as e:
            print(f"Error: {e}")

    # Now let's find the proper warehouse/raw material tables used in the 2026 system
    # If the dashboard uses sm_kontr_sat, what table does it use for raw materials?
    # Let's search tables matching '%material%' or '%xammal%' that have dates in 2026.
    print("\n--- Searching for Material Tables with 2026 Data ---")
    
    cursor.execute("SELECT name FROM sys.tables WHERE name LIKE '%xammal%' OR name LIKE '%material%' OR name LIKE '%anbar%' OR name LIKE '%depo%' OR name LIKE '%stok%'")
    mat_tables = [r[0] for r in cursor.fetchall()]
    
    for t in mat_tables:
        try:
            # check if it has a date column
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{t}' AND (column_name LIKE '%date%' OR column_name LIKE '%tarix%')")
            date_cols = [r[0] for r in cursor.fetchall()]
            
            if date_cols:
                date_col = date_cols[0]
                cursor.execute(f"SELECT TOP 1 {date_col} FROM {t} ORDER BY idn DESC")
                res = cursor.fetchone()
                if res and res[0] and '2026' in str(res[0]):
                    print(f"Found 2026 data in table: {t} (Column: {date_col}, Latest: {res[0]})")
        except Exception:
            pass

    conn.close()

if __name__ == "__main__":
    verify_recent_data()
