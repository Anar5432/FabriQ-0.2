import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socks_dashboard.settings')
django.setup()
from dashboard.queries import query

for phase in [1, 4, 5]:
    sql = f'''
    SELECT TOP 3 
        i.idn as record_id, 
        i.tarix as date, 
        g.name as product_name, 
        e.miqdar as qty,
        i.serh as comment,
        f.name as phase_name
    FROM sm_good_ist i WITH (NOLOCK)
    JOIN sm_good_ist_el e WITH (NOLOCK) ON e.es_no = i.idn
    JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
    JOIN sm_faza f WITH (NOLOCK) ON e.son_faza = f.idn
    WHERE g.class IN (21, 29, 30) AND e.son_faza = {phase}
    ORDER BY i.tarix DESC
    '''
    res = query(sql)
    print(f"\n--- Phase {phase} Examples ---")
    for r in res:
        pname = (r['product_name'] or '').encode('ascii', 'ignore').decode('ascii')
        comment = (r['comment'] or '').encode('ascii', 'ignore').decode('ascii')
        print(f"Record: {r['record_id']} | Date: {str(r['date'])[:10]} | Product: {pname} | Qty: {r['qty']} | Comment: {comment}")
