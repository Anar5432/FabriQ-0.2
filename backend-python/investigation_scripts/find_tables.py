import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import query

def check_logic():
    out = io.StringIO()
    out.write("Finding tables with 'satis'...\n")
    q1 = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%satis%'"
    rows1 = query(q1)
    for r in rows1: out.write(f"{r}\n")

    out.write("\nFinding tables with 'sifaris'...\n")
    q2 = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%sifaris%'"
    rows2 = query(q2)
    for r in rows2: out.write(f"{r}\n")

    with io.open("tables_out.txt", "w", encoding="utf-8") as f:
        f.write(out.getvalue())

if __name__ == '__main__':
    check_logic()
