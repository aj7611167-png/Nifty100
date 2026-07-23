from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_top_roe():
    response = client.get("/api/v1/analytics/top-roe")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0


def test_company_scorecard():
    response = client.get(
        "/api/v1/analytics/company-scorecard?company_id=ABB"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "ABB"


def test_rankings():
    response = client.get(
        "/api/v1/analytics/rankings?metric=return_on_equity_pct"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_compare():
    response = client.get(
        "/api/v1/analytics/compare?company1=ABB&company2=ADANIENT"
    )

    assert response.status_code == 200

    data = response.json()

    assert "company1" in data

    assert "company2" in data