import pyodbc
from dashboard.erp_connector import get_connection

def find_warehouse_tables():
    conn = get_connection()
    if not conn:
        print("Could not connect to database")
        return

    cursor = conn.cursor()
    # Find all tables and their columns in the database
    query = """
    SELECT 
        t.name AS table_name,
        c.name AS column_name
    FROM 
        sys.tables t
    INNER JOIN 
        sys.columns c ON t.object_id = c.object_id
    WHERE 
        t.name LIKE '%ambar%' OR 
        t.name LIKE '%material%' OR 
        t.name LIKE '%stok%' OR 
        t.name LIKE '%depo%' OR 
        t.name LIKE '%transfer%' OR
        t.name LIKE '%xammal%' OR
        t.name LIKE '%kesim%' OR
        t.name LIKE '%req%' OR
        t.name LIKE '%sifaris%' OR
        t.name LIKE '%order%'
    ORDER BY 
        t.name, c.column_id;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    tables = {}
    for row in rows:
        t_name = row[0]
        c_name = row[1]
        if t_name not in tables:
            tables[t_name] = []
        tables[t_name].append(c_name)
        
    for t_name, cols in tables.items():
        print(f"Table: {t_name}")
        print(f"Columns: {', '.join(cols)}")
        print("-" * 40)
        
    if not tables:
        print("No matching tables found. Let's list all tables instead:")
        cursor.execute("SELECT name FROM sys.tables ORDER BY name")
        all_tables = [r[0] for r in cursor.fetchall()]
        print(", ".join(all_tables))

    conn.close()

if __name__ == "__main__":
    find_warehouse_tables()
