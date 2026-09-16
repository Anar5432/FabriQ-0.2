import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('C:/Users/User/.gemini/antigravity/scratch/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socks_dashboard.settings'
import django
django.setup()

from dashboard.queries import query

sql = """
    SELECT top 1 name FROM sm_kontra WITH (NOLOCK) WHERE idn = 840
"""
res = query(sql)
print("sm_kontra 840:", res)

sql_kafe = """
    SELECT top 1 name FROM sm_kontra_kafe WITH (NOLOCK) WHERE idn = 840
"""
try:
    print("sm_kontra_kafe 840:", query(sql_kafe))
except Exception as e:
    print(e)
    
sql_sat = """
    SELECT top 1 kontra_name FROM sm_kontr_sat WITH (NOLOCK) WHERE kontra = 840 AND kontra_name IS NOT NULL
"""
try:
    print("sm_kontr_sat 840:", query(sql_sat))
except Exception as e:
    pass
    
sql_sif_sat = """
    SELECT top 1 kontra_name FROM sm_kontr_sif_sat WITH (NOLOCK) WHERE kontra = 840 AND kontra_name IS NOT NULL
"""
try:
    print("sm_kontr_sif_sat 840:", query(sql_sif_sat))
except Exception as e:
    pass

