import pyodbc

SERVER = '81.17.87.85,1433'
DATABASE = 'BTFERPDB'
USERNAME = 'User1'
PASSWORD = 'bfzY7835WCS72M'

def get_connection():
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def main():
    conn = get_connection()
    
    print("--- SM_BORC (Debt / AR & AP) ---")
    cursor = conn.cursor()
    cursor.execute("SELECT nov, COUNT(*) as cnt, SUM(yekun) as total_yekun FROM sm_borc GROUP BY nov")
    for row in cursor.fetchall():
        print(row)
    
    print("\n--- SM_BANK_OD (Bank Payments / Cash Flow) ---")
    cursor.execute("SELECT COUNT(*) as cnt, SUM(med_meb) as total_in, SUM(mex_meb) as total_out FROM sm_bank_od")
    for row in cursor.fetchall():
        print(row)
    
    print("\n--- SM_KMD_EL (Invoice Balances) ---")
    cursor.execute("SELECT COUNT(*) as cnt, SUM(mebleg) as total_mebleg, SUM(odenen) as total_odenen, SUM(qaliq) as total_qaliq FROM sm_kmd_el")
    for row in cursor.fetchall():
        print(row)

    print("\n--- SM_KMD (Cash/Expense/Income maybe?) ---")
    try:
        cursor.execute("SELECT nov, COUNT(*) as cnt, SUM(mebleg) as total_mebleg FROM sm_kmd GROUP BY nov")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print("sm_kmd error:", e)

    print("\n--- SM_SIFARIS_QAIME (Sales/Invoices) ---")
    try:
        cursor.execute("SELECT COUNT(*) as cnt, SUM(mebleg) as total_mebleg, SUM(yekun) as total_yekun FROM sm_sifaris_qaime")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print("sm_sifaris_qaime error:", e)

    # Let's get some top row samples of sm_kmd to see what it is
    try:
        print("\n--- SM_KMD Samples ---")
        cursor.execute("SELECT TOP 2 * FROM sm_kmd")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        pass

if __name__ == '__main__':
    main()
