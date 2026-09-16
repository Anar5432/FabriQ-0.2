import pyodbc
import re

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

    keywords = ['kmd', 'kmx', 'bmd', 'bmx', 'medax', 'mexar', 'kassa', 'bank', 'hesab']
    
    cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = cursor.fetchall()
    
    accounting_tables = []
    for schema, tname in tables:
        tname_lower = tname.lower()
        # exact matches or contains
        if any(kw in tname_lower for kw in keywords) or tname_lower in ['sm_kmd', 'sm_kmx', 'sm_bmd', 'sm_bmx']:
            accounting_tables.append((schema, tname))

    results = []
    
    for schema, tname in accounting_tables:
        full_tname = f"[{schema}].[{tname}]"
        
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {full_tname}")
            row_count = cursor.fetchone()[0]
        except Exception:
            continue
            
        if row_count == 0:
            continue
            
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{tname}'")
        columns = cursor.fetchall()
        date_columns = [c.COLUMN_NAME for c in columns if c.DATA_TYPE in ('date', 'datetime', 'datetime2', 'smalldatetime')]
        
        last_updated = None
        if date_columns:
            max_dates = []
            for dcol in date_columns:
                try:
                    cursor.execute(f"SELECT MAX([{dcol}]) FROM {full_tname}")
                    res = cursor.fetchone()
                    if res and res[0]:
                        max_dates.append(res[0])
                except Exception:
                    pass
            if max_dates:
                last_updated = max(max_dates)
                
        if last_updated and str(last_updated) > '2025-01-01':
            results.append({
                'schema': schema,
                'table': tname,
                'row_count': row_count,
                'last_updated': last_updated
            })
        elif not last_updated: # Check if it is a detail table of an active table
            results.append({
                'schema': schema,
                'table': tname,
                'row_count': row_count,
                'last_updated': 'Unknown (No date column)'
            })

    results.sort(key=lambda r: str(r['last_updated']), reverse=True)
    
    with open('accounting_research2.txt', 'w', encoding='utf-8') as f:
        for r in results:
            f.write(f"{r['schema']}.{r['table']} | Rows: {r['row_count']} | Last updated: {r['last_updated']}\n")

if __name__ == '__main__':
    main()
