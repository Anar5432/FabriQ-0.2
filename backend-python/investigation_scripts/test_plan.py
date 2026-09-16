import json
from fastapi.testclient import TestClient
from main import app, seed_db

# Make sure db is seeded
seed_db()

client = TestClient(app)

def test_plan():
    response = client.post(
        "/api/plan",
        json={
            "orders": [
                {
                    "order_id": "ORD-101",
                    "workers": 15,
                    "difficulty": "easy"
                }
            ]
        }
    )
    print("Plan Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        apply_response = client.post(
            "/api/apply_plan",
            json={"plans": response.json()["results"]}
        )
        print("Apply Response:")
        print(json.dumps(apply_response.json(), indent=2))

if __name__ == "__main__":
    test_plan()
