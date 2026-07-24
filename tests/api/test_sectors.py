from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_sectors():
    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 10

    names = [row["broad_sector"] for row in data]

    assert "Information Technology" in names
    assert "Financials" in names


def test_it_sector():
    response = client.get("/api/v1/sectors/IT/companies")

    assert response.status_code == 200

    companies = response.json()

    assert len(companies) > 0

    for company in companies:
        assert company["broad_sector"] == "Information Technology"


def test_invalid_sector():
    response = client.get("/api/v1/sectors/INVALID/companies")

    assert response.status_code == 404