"""
Unit tests for Core Analytics & Arrhenius Kinetics Engine
"""

from analytics.spoilage_engine import calculate_spoilage_metrics
from analytics.arbitrage_engine import evaluate_arbitrage_opportunity
from analytics.loss_estimator import calculate_financial_and_carbon_loss
from analytics.health_engine import calculate_container_health


def test_spoilage_metrics_normal_temperature():
    telemetry = {
        "container_id": "TEST-101",
        "commodity": "Avocados",
        "temperature": 5.0,
        "humidity": 85.0,
        "door_open": False
    }
    result = calculate_spoilage_metrics(telemetry)
    assert result["freshness_index_pct"] >= 60.0
    assert result["spoilage_risk_score_pct"] <= 40.0
    assert result["is_cold_chain_violation"] is False


def test_spoilage_metrics_thermal_excursion():
    telemetry = {
        "container_id": "TEST-102",
        "commodity": "Strawberries",
        "temperature": 12.5,  # Extreme temp excursion!
        "humidity": 88.0,
        "door_open": True
    }
    result = calculate_spoilage_metrics(telemetry)
    assert result["spoilage_risk_score_pct"] > 50.0
    assert result["is_cold_chain_violation"] is True
    assert result["door_open_breach"] is True


def test_arbitrage_opportunity_calculation():
    telemetry = {
        "container_id": "TEST-103",
        "shipment_id": "SHP-001",
        "commodity": "Avocados",
        "temperature": 8.5,
        "destination": "Rotterdam Port",
        "market_price": 3.40,
        "remaining_distance_km": 1200,
        "gps_speed": 30.0,
        "alternative_destinations": [
            {"name": "Antwerp Port", "extra_km": -150}
        ]
    }
    arb = evaluate_arbitrage_opportunity(telemetry)
    assert "arbitrage_score" in arb
    assert "max_net_profit_delta_usd" in arb
    assert "recommendation" in arb


def test_container_health_score():
    telemetry = {
        "container_id": "TEST-104",
        "battery": 10.0,  # Critical low battery
        "door_open": True,
        "sensor_health": "DEGRADED"
    }
    health = calculate_container_health(telemetry)
    assert health["container_health_score_pct"] < 60.0
    assert len(health["active_anomalies"]) >= 2
