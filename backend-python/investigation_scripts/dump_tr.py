import re
with open('rendered.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<tr onclick="openModal(.*?)</tr>', content, re.DOTALL)
if match:
    with open('single_tr.html', 'w', encoding='utf-8') as f:
        f.write(match.group(0))
