import os
import sys
import django

sys.path.append(r'c:\Users\User\.gemini\antigravity\scratch\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from django.test import Client
c = Client()
response = c.get('/?sector=isci')

with open('rendered.html', 'wb') as f:
    f.write(response.content)

print(f"Size: {len(response.content)} bytes")
