import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabriq.settings')
django.setup()

from dashboard.erp_connector import query

orders = query('''
    SELECT 
        t.sen_no, 
        t.serh AS company, 
        g.name AS product, 
        tel.miqdar, 
        tel.qaliq, 
        tel.teslim 
    FROM sm_sifaris t 
    JOIN sm_sifaris_el tel ON t.idn = tel.es_no
    JOIN sm_goods g ON tel.mal = g.idn
    WHERE t.sen_no IN ('022386', '022343')
''')
for row in orders:
    print(row)
