# -*- coding: utf-8 -*-
import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.queries import get_orders

def check_logic():
    out = io.StringIO()
    try:
        data = get_orders('isci')
        out.write(f"Success! Found {len(data['companies'])} companies.\n")
    except Exception as e:
        out.write(f"Error: {e}\n")

    with io.open("fix_keys.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
