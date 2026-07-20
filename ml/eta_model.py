"""
AtmoSync Transit Delay & ETA Regression Model
Estimates remaining transit hours, arrival timestamp, and delay risk based on vessel speed, 
remaining distance, weather severity, port congestion, and cold-chain hold alerts.
"""

from datetime import datetime, timedelta
from typing import Dict, Any


class ETAPredictor:
    """
    Transit duration & arrival delay regressor.
    """

    def predict_eta(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates predicted arrival datetime, remaining transit hours, and delay likelihood.
        """
        speed_kmh = float(telemetry.get("gps_speed_kmh", 50.0))
        remaining_km = float(telemetry.get("remaining_distance_km", 450.0))
        weather = str(telemetry.get("ambient_weather", "Clear")).lower()
        spoilage_risk = float(telemetry.get("spoilage_risk_score_pct", 15.0))

        if speed_kmh <= 1.0:
            effective_speed = 35.0  # Default assumed average cruising speed when stationary/idle
        else:
            effective_speed = speed_kmh

        # Base time calculation
        base_hours_remaining = remaining_km / max(5.0, effective_speed)

        # Weather slowdown factor
        weather_delay_factor = 1.0
        if "storm" in weather or "rain" in weather:
            weather_delay_factor = 1.25
        elif "fog" in weather or "wind" in weather:
            weather_delay_factor = 1.12

        # Cold chain inspection hold factor if high spoilage risk
        inspection_delay_hours = 0.0
        if spoilage_risk > 60.0:
            inspection_delay_hours = 2.5  # Priority inspection queue delay

        total_remaining_hours = round((base_hours_remaining * weather_delay_factor) + inspection_delay_hours, 1)

        now = datetime.now()
        predicted_arrival = now + timedelta(hours=total_remaining_hours)

        # Baseline scheduled ETA
        baseline_remaining_hours = remaining_km / 50.0
        scheduled_arrival = now + timedelta(hours=baseline_remaining_hours)

        delay_hours = round(total_remaining_hours - baseline_remaining_hours, 1)

        return {
            "container_id": telemetry.get("container_id", "UNKNOWN"),
            "remaining_distance_km": remaining_km,
            "current_speed_kmh": speed_kmh,
            "predicted_remaining_hours": total_remaining_hours,
            "predicted_arrival_iso": predicted_arrival.isoformat(),
            "scheduled_arrival_iso": scheduled_arrival.isoformat(),
            "estimated_delay_hours": delay_hours,
            "delay_risk_status": "HIGH_DELAY" if delay_hours > 3.0 else ("MODERATE_DELAY" if delay_hours > 1.0 else "ON_SCHEDULE"),
            "weather_impact_factor": weather_delay_factor
        }


eta_predictor = ETAPredictor()

if __name__ == "__main__":
    test_data = {
        "container_id": "CONT-2004",
        "gps_speed_kmh": 42.0,
        "remaining_distance_km": 680.0,
        "ambient_weather": "Heavy Rain & Wind",
        "spoilage_risk_score_pct": 72.0
    }
    res = eta_predictor.predict_eta(test_data)
    print("ETA Predictor Test Result:", res)
