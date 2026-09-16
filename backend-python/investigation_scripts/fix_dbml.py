import sys

filepath = 'C:/Users/User/.gemini/antigravity/scratch/backend/BTFERPDB_schema.dbml'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix literal escaped newlines and quotes
text = text.replace('\\n', '\n')
text = text.replace('\\"', '"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("DBML cleaned successfully!")
