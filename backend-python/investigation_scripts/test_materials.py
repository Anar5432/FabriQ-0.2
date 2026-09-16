import os
from database import SessionLocal
from main import plan_materials
import json

db = SessionLocal()
try:
    results = plan_materials(db)
    # The result is a list of OrderMaterialPlanning (pydantic objects or dicts depending on FastAPI response)
    if results and hasattr(results[0], "dict"):
        print(json.dumps([r.dict() for r in results], indent=2))
    else:
        print(json.dumps(results, indent=2))
finally:
    db.close()
