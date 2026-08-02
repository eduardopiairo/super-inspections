from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_template():
    payload = {
        "title": "Fire Safety",
        "description": "Basic fire safety checks",
        "sections": [
            {
                "title": "Extinguishers",
                "order": 1,
                "questions": [
                    {"text": "Is the extinguisher charged?", "order": 1, "response_type": "yes_no"}
                ],
            }
        ],
    }

    create_response = client.post("/templates/", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Fire Safety"
    assert len(created["sections"]) == 1

    get_response = client.get(f"/templates/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Fire Safety"


def test_get_template_not_found():
    response = client.get("/templates/999")
    assert response.status_code == 404
