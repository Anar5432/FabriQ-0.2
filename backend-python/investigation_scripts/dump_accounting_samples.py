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

    tables = ['sm_kmd', 'sm_kmx', 'sm_kmd_el', 'sm_kmx_el', 'sm_bank_od', 'sm_bank_od_el', 'sm_kassa_transfer']
    
    with open('accounting_samples.txt', 'w', encoding='utf-8') as f:
        for tname in tables:
            f.write(f"--- TABLE: {tname} ---\n")
            try:
                cursor.execute(f"SELECT COUNT(*) FROM dbo.{tname}")
                count = cursor.fetchone()[0]
                f.write(f"Row count: {count}\n")
                if count > 0:
                    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tname}'")
                    cols = [row.COLUMN_NAME for row in cursor.fetchall()]
                    f.write(f"Columns: {', '.join(cols)}\n")
                    cursor.execute(f"SELECT TOP 1 * FROM dbo.{tname}")
                    sample = cursor.fetchone()
                    sample_dict = dict(zip(cols, sample)) if sample else {}
                    f.write(f"Sample: {sample_dict}\n")
            except Exception as e:
                f.write(f"Error: {e}\n")
            f.write("\n")

if __name__ == '__main__':
    main()
