import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

query = """
SELECT TOP 10 f.idn, f.sen_no as order_no, f.tarix, f.kontra, c.name as customer, f.serh
FROM sm_sifaris_form f
LEFT JOIN sm_kontra c ON f.kontra = c.idn
ORDER BY f.tarix DESC
"""
cursor.execute(query)
with codecs.open('links_output.txt', 'w', 'utf-8') as f:
    f.write("--- Recent sm_sifaris_form ---\n")
    for r in cursor.fetchall():
        f.write(f"{r}\n")

    # Check recent sm_smeta
    cursor.execute("SELECT TOP 10 idn, sen_no, sorgu, teklif, is_ad FROM sm_smeta ORDER BY tarix DESC")
    f.write("\n--- Recent sm_smeta ---\n")
    for r in cursor.fetchall():
        f.write(f"{r}\n")


conn.close()
