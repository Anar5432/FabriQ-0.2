import re
content=open('BTFERPDB_Active_Schema.dbml', encoding='utf-8').read()
tables=re.findall(r'Table\s+"([^"]+)"', content)
open('tables_list.txt','w', encoding='utf-8').write('\n'.join(tables))
