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
    cursor = conn.cursor()

    # 1. Does sm_kontr_sat have a 'odenen' or 'qaliq' column directly?
    try:
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_kontr_sat'")
        cols = [r.COLUMN_NAME for r in cursor.fetchall()]
        print("sm_kontr_sat columns:", cols)
    except Exception as e:
        print(e)
        
    # 2. How to get overall customer debt? 
    # Let's see if sm_borc gives correct balance per customer
    try:
        cursor.execute("""
            SELECT TOP 5 kontra, kon_name, mebleg, yekun
            FROM sm_borc
            ORDER BY tarix DESC
        """)
        rows = cursor.fetchall()
        print("\nRecent sm_borc records:")
        for r in rows:
            print(r)
    except Exception as e:
        print(e)

    # 3. How to get payment per order?
    # Let's check sm_kmd_el and sm_bank_od_el_el
    try:
        cursor.execute("""
            SELECT TOP 5 e.idn, e.qaime, e.kontra, e.mebleg, e.odenen, e.qaliq, s.sen_no, s.tarix
            FROM sm_bank_od_el_el e
            JOIN sm_kontr_sat s ON e.qaime = s.idn
        """)
        rows = cursor.fetchall()
        print("\nsm_bank_od_el_el joined with sm_kontr_sat:")
        for r in rows:
            print(r)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
