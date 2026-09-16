from dashboard.erp_connector import query
import json
try:
    orders = query("SELECT t.sen_no FROM sm_sifaris t WHERE t.sen_no = '004181'")
    print('sm_sifaris:', orders)
    orders2 = query("SELECT t.sen_no FROM sm_sifaris_form t WHERE t.sen_no = '004181'")
    print('sm_sifaris_form:', orders2)
    orders3 = query("SELECT t.sen_no FROM sm_sif_sened t WHERE t.sen_no = '004181'")
    print('sm_sif_sened:', orders3)
    orders4 = query("SELECT t.sen_no FROM sm_kontr_sat t WHERE t.sen_no = '004181'")
    print('sm_kontr_sat:', orders4)
except Exception as e:
    print(e)
