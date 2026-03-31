from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_api() -> None:
    response = client.post(
        "/analyze",
        json={
            "patient_id": "P001",
            "age": 56,
            "gender": "male",
            "history": ["diabetes"],
            "labs": {"scr": 145, "egfr": 52, "acr": 120, "urine_protein": "positive", "sbp": 148, "dbp": 92},
        },
    )
    assert response.status_code == 200
