import pyodbc
import re

SERVER = '81.17.87.85,1433'
DATABASE = 'BTFERPDB'
USERNAME = 'User1'
PASSWORD = 'bfzY7835WCS72M'

def get_connection():
    # Define connection string using the standard SQL Server driver or ODBC Driver 17
    # Note: On windows, "SQL Server" driver is generally available
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

    # Keywords for accounting, bank, payment
    keywords = ['bank', 'pay', 'account', 'hesab', 'muhasibat', 'odeni', 'kassa', 'kasa', 'cash', 'invoice', 'fatura', 'odenis']
    
    # 1. Get all user tables
    cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = cursor.fetchall()
    
    accounting_tables = []
    for schema, tname in tables:
        tname_lower = tname.lower()
        if any(kw in tname_lower for kw in keywords):
            accounting_tables.append((schema, tname))

    print(f"Found {len(accounting_tables)} potential accounting tables.")

    results = []
    
    for schema, tname in accounting_tables:
        full_tname = f"[{schema}].[{tname}]"
        
        # Check row count
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {full_tname}")
            row_count = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error counting {full_tname}: {e}")
            continue
            
        if row_count == 0:
            continue
            
        # Get column names to find date columns and to show sample data
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{tname}'")
        columns = cursor.fetchall()
        
        date_columns = [c.COLUMN_NAME for c in columns if c.DATA_TYPE in ('date', 'datetime', 'datetime2', 'smalldatetime')]
        
        last_updated = None
        if date_columns:
            # Query max of date columns
            max_dates = []
            for dcol in date_columns:
                try:
                    cursor.execute(f"SELECT MAX([{dcol}]) FROM {full_tname}")
                    res = cursor.fetchone()
                    if res and res[0]:
                        max_dates.append(res[0])
                except Exception as e:
                    pass
            if max_dates:
                # remove any strings, keep only actual dates/datetimes and get max
                last_updated = max(max_dates)
                
        # Get one sample row
        try:
            cursor.execute(f"SELECT TOP 1 * FROM {full_tname}")
            sample = cursor.fetchone()
            sample_dict = dict(zip([c.COLUMN_NAME for c in columns], sample)) if sample else {}
        except Exception as e:
            sample_dict = {}
            
        # If it's updated in 2024 or later, consider it active
        # Wait, let's just log everything that has rows, we can filter in the script
        results.append({
            'schema': schema,
            'table': tname,
            'row_count': row_count,
            'last_updated': last_updated,
            'columns': [c.COLUMN_NAME for c in columns],
            'sample': sample_dict
        })
        print(f"Checked {full_tname}: {row_count} rows, Last updated: {last_updated}")
        
    # Sort results by last_updated (descending)
    def get_sort_key(r):
        return r['last_updated'] if r['last_updated'] is not None else ''
        
    results.sort(key=lambda r: str(get_sort_key(r)), reverse=True)
    
    with open('accounting_research.txt', 'w', encoding='utf-8') as f:
        for r in results:
            f.write(f"--- TABLE: {r['schema']}.{r['table']} ---\n")
            f.write(f"Row count: {r['row_count']}\n")
            f.write(f"Last updated: {r['last_updated']}\n")
            f.write(f"Columns: {', '.join(r['columns'])}\n")
            f.write(f"Sample: {r['sample']}\n\n")

if __name__ == '__main__':
    main()
