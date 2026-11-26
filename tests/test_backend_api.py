from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ResearchPilot", "demo": True}


def test_select_bands_is_explicitly_synthetic_demo():
    response = client.post(
        "/select-bands",
        json={"dataset": "PaviaU", "method": "fisher", "k": 10},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["demo"] is True
    assert payload["data_source"] == "synthetic"
    assert payload["k"] == 10
    assert len(payload["selected_bands"]) == 10
    assert "not a PaviaU experiment result" in payload["note"]


def test_select_bands_rejects_invalid_k():
    response = client.post(
        "/select-bands",
        json={"dataset": "PaviaU", "method": "fisher", "k": 0},
    )
    assert response.status_code == 422

