import re

with open('rendered.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total HTML size: {len(content)}")

# Count <tr> tags
print("Number of <tr onclick=: ", content.count('<tr onclick="openModal'))

# Extract all tr lengths
matches = re.finditer(r'<tr onclick="openModal(.*?)</tr>', content, re.DOTALL)
lengths = [len(m.group(0)) for m in matches]
print(f"Average tr length: {sum(lengths) / len(lengths) if lengths else 0}")
print(f"Total tr length: {sum(lengths)}")

# Check what else is taking space
print("Number of companies: ", content.count('class="co-card company-card"'))

