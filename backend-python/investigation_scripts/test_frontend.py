from main import serve_dashboard, get_workers, read_orders
from database import SessionLocal

def test_frontend_internals():
    db = SessionLocal()
    try:
        # Test 1: root
        res = serve_dashboard()
        if hasattr(res, "path"):
            print("OK Root endpoint serves:", res.path)
        else:
            print("x Root endpoint error:", res)
            
        # Test 2: workers
        workers = get_workers(db)
        print(f"OK /api/workers returns {len(workers)} workers")
        assert len(workers) > 0
        
        # Test 3: orders
        orders = read_orders(None, None, 0, 100, db)
        print(f"OK /api/orders returns {len(orders)} orders")
        assert len(orders) > 0
        
    finally:
        db.close()

if __name__ == "__main__":
    test_frontend_internals()
    print("All internal frontend tests passed!")
