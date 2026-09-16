import os
import json
from database import SessionLocal
from main import assign_worker, AssignWorkerRequest, get_planning_details, seed_db

def test():
    db = SessionLocal()
    try:
        # DB will be empty and seed_db wasn't explicitly called at module import, 
        # but main.py has `seed_db()` at the top. Let's explicitly call it to be safe.
        # Actually it's called during module import in main.py, but just in case.
        
        # Test assign_worker for ORD-201 (Polo T-Shirt)
        # ORD-201 has qty 5,000. Stages: t1, t2, t3.
        # w1 has t1 (cap: 1000). Needs 5 days.
        # w2 has t2 (cap: 800). Needs 7 days.
        
        req1 = AssignWorkerRequest(order_id="ORD-201", stage_id="t1", worker_id="w1")
        res1 = assign_worker(req1, db)
        print("Stage t1 assigned:", res1)
        
        req2 = AssignWorkerRequest(order_id="ORD-201", stage_id="t2", worker_id="w2")
        res2 = assign_worker(req2, db)
        print("Stage t2 assigned:", res2)
        
        details = get_planning_details("ORD-201", db)
        print("\nPlanning Details for ORD-201:")
        print(json.dumps(details, indent=2, default=str))
        
    finally:
        db.close()

if __name__ == "__main__":
    test()
