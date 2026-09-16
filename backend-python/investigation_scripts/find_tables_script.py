import re

content = open('BTFERPDB_Active_Schema.dbml', encoding='utf-8').read()
tables = re.findall(r'Table\s+"([^"]+)"\s+\{([^}]+)\}', content)

kws = ['sif', 'smeta', 'qaliq', 'anbar', 'rasen', 'isci', 'faza', 'stage', 'emp']

matches = {kw: [] for kw in kws}

for t_name, cols in tables:
    for kw in kws:
        if kw in t_name.lower():
            matches[kw].append((t_name, cols.strip()))

for kw, items in matches.items():
    print(f'=== {kw.upper()} ===')
    for t_name, cols in items:
        print(f'Table: {t_name}')
        # print some of the columns to get the idea
        col_lines = cols.split('\n')
        print('\n'.join(col_lines))
        print('------------------')
    print('\n')
