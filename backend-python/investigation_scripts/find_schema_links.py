import os
import django
import codecs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()

from dashboard.erp_connector import get_connection

conn = get_connection()
cursor = conn.cursor()

def dump_cols(table):
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
    return [row[0] for row in cursor.fetchall()]

print("sm_sifaris_el:", dump_cols("sm_sifaris_el"))
print("sm_kontr_sat_el:", dump_cols("sm_kontr_sat_el"))
print("sm_rasc:", dump_cols("sm_rasc"))
print("sm_rasc_el:", dump_cols("sm_rasc_el"))
print("sm_smeta_emek:", dump_cols("sm_smeta_emek"))
print("sm_goods:", dump_cols("sm_goods"))

# Find latest 5 orders in sm_sifaris_form
cursor.execute("SELECT TOP 5 idn, sen_no, tarix, serh, status, status_ad FROM sm_sifaris_form ORDER BY tarix DESC")
print("\nLatest 5 sifaris_form:")
for row in cursor.fetchall():
    print(row)

# Find latest 5 in sm_kontr_sat
cursor.execute("SELECT TOP 5 idn, sen_no, tarix, tam_yek FROM sm_kontr_sat ORDER BY tarix DESC")
print("\nLatest 5 kontr_sat:")
for row in cursor.fetchall():
    print(row)

conn.close()
