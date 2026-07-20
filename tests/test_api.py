"""
Integration tests for FastAPI endpoints
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ONLINE"


def test_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "active_containers" in data
    assert "total_cargo_valuation_usd" in data


def test_containers_list():
    response = client.get("/api/containers")
    assert response.status_code == 200
    data = response.json()
    assert "containers" in data
    assert data["count"] > 0


def test_spoilage_analytics():
    response = client.get("/api/spoilage")
    assert response.status_code == 200
    assert "high_spoilage_risk_count" in response.json()


def test_arbitrage_route():
    response = client.get("/api/arbitrage")
    assert response.status_code == 200
    assert "total_potential_arbitrage_gain_usd" in response.json()


def test_ml_metrics():
    response = client.get("/api/ml/metrics")
    assert response.status_code == 200
    assert "performance_metrics" in response.json()


def test_reports_download_csv():
    response = client.get("/api/reports/download?format=csv")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
