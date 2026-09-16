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

    sql = """
    SELECT TOP 10
        s.idn AS order_id,
        s.sen_no,
        s.kontra_name,
        s.tam_yek AS total_amount,
        ISNULL(bank_pay.total_odenen, 0) + ISNULL(cash_pay.total_odenen, 0) AS paid_amount,
        s.tam_yek - (ISNULL(bank_pay.total_odenen, 0) + ISNULL(cash_pay.total_odenen, 0)) AS remaining_balance
    FROM sm_kontr_sat s
    LEFT JOIN (
        SELECT qaime, SUM(odenen) AS total_odenen
        FROM sm_bank_od_el_el
        GROUP BY qaime
    ) bank_pay ON s.idn = bank_pay.qaime
    LEFT JOIN (
        SELECT qaime, SUM(odenen) AS total_odenen
        FROM sm_kmd_el
        GROUP BY qaime
    ) cash_pay ON s.idn = cash_pay.qaime
    WHERE (ISNULL(bank_pay.total_odenen, 0) + ISNULL(cash_pay.total_odenen, 0)) > 0
    ORDER BY s.tarix DESC
    """
    
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("Orders with Payments:")
        for r in rows:
            print(f"Order {r.sen_no} ({r.kontra_name}): Total: {r.total_amount}, Paid: {r.paid_amount}, Remaining: {r.remaining_balance}")
    except Exception as e:
        print(e)
        
    sql_cust = """
    SELECT TOP 10 kontra, kon_name, MAX(tarix), SUM(yekun)
    FROM sm_borc
    GROUP BY kontra, kon_name
    ORDER BY MAX(tarix) DESC
    """
    try:
        cursor.execute(sql_cust)
        rows = cursor.fetchall()
        print("\nCustomer Balances:")
        for r in rows:
            # handle charmap issue
            name = r.kon_name.encode('utf-8', 'replace').decode('utf-8') if r.kon_name else ''
            print(f"Cust {r.kontra} ({name}): Balance: {r[3]}")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
