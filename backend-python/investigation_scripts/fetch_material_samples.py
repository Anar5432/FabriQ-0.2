import pyodbc
from dashboard.erp_connector import get_connection

def fetch_samples():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    
    tables = ['sm_sifaris_qaime', 'sm_sifaris_qaime_el_el', 'sm_good_ist_xammal', 'sm_xammal_plan_cem', 'sm_depo']
    
    for table in tables:
        print(f"--- Top 3 rows from {table} ---")
        try:
            cursor.execute(f"SELECT TOP 3 * FROM {table} ORDER BY idn DESC")
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            print(" | ".join(columns))
            for row in rows:
                print(" | ".join(str(val) for val in row))
        except Exception as e:
            print(f"Error querying {table}: {e}")
        print("\n")

    conn.close()

if __name__ == "__main__":
    fetch_samples()
