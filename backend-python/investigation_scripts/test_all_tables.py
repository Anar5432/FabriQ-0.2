from dashboard.erp_connector import query
tables = query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME = 'sen_no'")
for row in tables:
    try:
        res = query(f"SELECT sen_no FROM {row['TABLE_NAME']} WHERE sen_no = '004181' OR sen_no = '4181'")
        if res:
            print(f"FOUND IN {row['TABLE_NAME']}")
    except:
        pass
