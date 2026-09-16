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

    keywords = ['borc', 'qaliq', 'balans', 'musteri', 'client', 'hesab', 'qaime', 'invoice']
    
    cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = cursor.fetchall()
    
    target_tables = []
    for schema, tname in tables:
        tname_lower = tname.lower()
        if any(kw in tname_lower for kw in keywords) or tname_lower in ['sm_kmd_el', 'sm_bank_od_el_el']:
            target_tables.append((schema, tname))

    with open('customer_balance_research.txt', 'w', encoding='utf-8') as f:
        f.write("--- FOUND TABLES WITH KEYWORDS ---\n")
        
        # Filter to those with rows
        for schema, tname in target_tables:
            full_tname = f"[{schema}].[{tname}]"
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {full_tname}")
                count = cursor.fetchone()[0]
                if count > 0:
                    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tname}'")
                    cols = [row.COLUMN_NAME for row in cursor.fetchall()]
                    
                    # only keep interesting ones that seem relevant to customer debts
                    if any(c.lower() in ('qaliq', 'borc', 'odenen', 'mebleg', 'kontra') for c in cols) or 'balans' in tname.lower() or 'qaliq' in tname.lower():
                        f.write(f"\nTABLE: {tname} | Rows: {count}\n")
                        f.write(f"Columns: {', '.join(cols)}\n")
                        cursor.execute(f"SELECT TOP 1 * FROM {full_tname} ORDER BY idn DESC") # get latest
                        sample = cursor.fetchone()
                        sample_dict = dict(zip(cols, sample)) if sample else {}
                        f.write(f"Sample: {sample_dict}\n")
            except Exception as e:
                pass

if __name__ == '__main__':
    main()
