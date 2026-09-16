from dashboard.erp_connector import query
import json

cols = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris'")
print('sm_sifaris:', [r['COLUMN_NAME'] for r in cols])
cols2 = query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sm_sifaris_el'")
print('sm_sifaris_el:', [r['COLUMN_NAME'] for r in cols2])
