"""
Unit tests for Machine Learning Engine
"""

from ml.spoilage_model import spoilage_predictor
from ml.eta_model import eta_predictor
from ml.price_forecast import price_forecaster
from ml.explainability import explainability_engine


def test_spoilage_predictor():
    sample = {
        "container_id": "CONT-900",
        "temperature": 10.0,
        "max_temp": 6.0,
        "arrhenius_decay_ratio": 2.0,
        "door_open": True
    }
    pred = spoilage_predictor.predict_spoilage_risk(sample)
    assert "spoilage_probability_pct" in pred
    assert pred["risk_level"] in ["CRITICAL", "HIGH", "MODERATE", "LOW"]


def test_eta_predictor():
    sample = {
        "container_id": "CONT-901",
        "gps_speed_kmh": 45.0,
        "remaining_distance_km": 450.0,
        "ambient_weather": "Storm"
    }
    eta = eta_predictor.predict_eta(sample)
    assert "predicted_remaining_hours" in eta
    assert eta["predicted_remaining_hours"] > 0


def test_price_forecaster():
    fc = price_forecaster.forecast_prices("Avocados", days_ahead=5)
    assert fc["commodity"] == "Avocados"
    assert "Rotterdam" in fc["markets"]
    assert len(fc["markets"]["Rotterdam"]) == 5


def test_explainability_engine():
    exp = explainability_engine.explain_prediction({"container_id": "CONT-902", "temperature": 8.0, "max_temp": 5.0}, 65.0)
    assert "waterfall_attributions" in exp
    assert len(exp["waterfall_attributions"]) > 0
