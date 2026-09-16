from main import app, plan_orders, apply_plan
from database import SessionLocal
import schemas
import json

db = SessionLocal()
req = schemas.OrderPlanRequest(orders=[
    schemas.PlanOrderInput(order_id="CR-001", workers=15, difficulty="easy")
])

res = plan_orders(req, db)
print(json.dumps(res, indent=2, default=str))
