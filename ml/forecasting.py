"""
AtmoSync Forecasting Engine
Time-series and regression models for ETA delay predictions and commodity spot price trends.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor


class ForecastingEngine:
    """Forecasting models for shipment delays and market price trajectories."""

    def __init__(self):
        self.delay_model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.price_model = Ridge(alpha=1.0)
        self._fit_baseline_models()

    def _fit_baseline_models(self):
        # Synthetic training data for ETA Delay (hours)
        np.random.seed(42)
        X_delay = np.random.uniform([10, 100, 0], [45, 5000, 1], size=(500, 3))  # [speed, distance, weather_severity]
        y_delay = (X_delay[:, 1] / X_delay[:, 0]) * (1.0 + 0.3 * X_delay[:, 2]) - (X_delay[:, 1] / X_delay[:, 0])
        self.delay_model.fit(X_delay, y_delay)

        # Synthetic training for spot price trend ($/kg)
        X_price = np.random.uniform([1.0, 0, 5.0], [8.0, 1, 35.0], size=(500, 3))  # [base_price, seasonality, temp]
        y_price = X_price[:, 0] * (1.0 + 0.05 * np.sin(X_price[:, 1]) + 0.01 * X_price[:, 2])
        self.price_model.fit(X_price, y_price)

    def predict_delay(self, speed_kmh: float, distance_km: float, weather_condition: str) -> Dict[str, Any]:
        """Predict expected shipment delay in hours due to weather and speed."""
        weather_severity = 1.0 if weather_condition in ["Storm", "High Temperature Wave"] else 0.0
        features = np.array([[speed_kmh, distance_km, weather_severity]])
        predicted_delay_hrs = float(self.delay_model.predict(features)[0])

        return {
            "predicted_delay_hours": round(max(0.0, predicted_delay_hrs), 1),
            "delay_severity": "HIGH_DELAY" if predicted_delay_hrs > 4.0 else "ON_SCHEDULE"
        }

    def forecast_price_trend(self, base_price: float, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Forecast spot market prices over a 7-day horizon."""
        forecasts = []
        for d in range(1, days_ahead + 1):
            features = np.array([[base_price, d, 22.0]])
            projected_price = float(self.price_model.predict(features)[0]) + float(np.random.uniform(-0.1, 0.15))
            forecasts.append({
                "day_offset": d,
                "projected_price_usd_per_kg": round(max(0.5, projected_price), 2)
            })
        return forecasts


forecasting_engine = ForecastingEngine()


if __name__ == "__main__":
    print("Delay Prediction:", forecasting_engine.predict_delay(30.0, 2500, "Storm"))
    print("7-Day Forecast:", forecasting_engine.forecast_price_trend(3.40))
