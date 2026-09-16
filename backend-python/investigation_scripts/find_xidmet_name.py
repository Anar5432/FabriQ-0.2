import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.1.100;"
    "DATABASE=factory_erp;"
    "UID=sa;"
    "PWD=YourPassword123;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

try:
    cursor.execute("SELECT name FROM sm_goods WHERE idn = 11")
    row = cursor.fetchone()
    print("Goods 11:", row)
except:
    pass

try:
    cursor.execute("SELECT name FROM sm_xidmet WHERE idn = 11")
    row = cursor.fetchone()
    print("Xidmet 11:", row)
except:
    pass

try:
    cursor.execute("SELECT name, is_ad FROM sm_xidmet WHERE idn = 11")
    row = cursor.fetchone()
    print("Xidmet 11:", row)
except:
    pass
