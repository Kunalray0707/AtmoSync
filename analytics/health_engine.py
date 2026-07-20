"""
AtmoSync Container Health & Diagnostic Engine
Calculates holistic health scores (0-100%) for IoT containers based on sensor signals, battery levels, and thermal performance.
"""

from typing import Dict, Any


def calculate_container_health(telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes Container Health Score (0-100%), detecting sensor degradation,
    compressor strain, battery exhaustion, and door breach penalties.
    """
    battery = float(telemetry.get("battery", 100.0))
    door_open = bool(telemetry.get("door_open", False))
    sensor_status = str(telemetry.get("sensor_health", "HEALTHY")).upper()
    temp = float(telemetry.get("temperature", 5.0))
    ambient = float(telemetry.get("ambient_temperature", 25.0))
    
    # 1. Base Score starts at 100%
    health_score = 100.0
    anomalies = []
    
    # Battery Penalty
    if battery < 15.0:
        health_score -= 35.0
        anomalies.append("CRITICAL_BATTERY_LOW")
    elif battery < 30.0:
        health_score -= 15.0
        anomalies.append("BATTERY_LOW")
        
    # Door Open Penalty
    if door_open:
        health_score -= 20.0
        anomalies.append("DOOR_UNLATCHED")
        
    # Sensor Status Penalty
    if sensor_status == "MALFUNCTION":
        health_score -= 40.0
        anomalies.append("SENSOR_MALFUNCTION")
    elif sensor_status == "DEGRADED":
        health_score -= 20.0
        anomalies.append("SENSOR_CALIBRATION_DRIFT")
        
    # Thermal Differential Strain (Compressor workload check)
    temp_delta = ambient - temp
    if temp_delta > 30.0:  # High ambient heat strain
        health_score -= 10.0
        anomalies.append("EXTREME_AMBIENT_THERMAL_STRAIN")
        
    health_score = round(max(0.0, health_score), 1)
    
    # Diagnostic Status
    if health_score >= 85.0:
        status = "EXCELLENT"
    elif health_score >= 65.0:
        status = "ACCEPTABLE"
    elif health_score >= 40.0:
        status = "REQUIRES_MAINTENANCE"
    else:
        status = "CRITICAL_FAILURE_IMMORTAL"
        
    return {
        "container_id": telemetry.get("container_id"),
        "container_health_score_pct": health_score,
        "health_status": status,
        "battery_pct": battery,
        "sensor_health_raw": sensor_status,
        "active_anomalies": anomalies
    }


if __name__ == "__main__":
    t = {"container_id": "CONT-1004", "battery": 12.0, "door_open": True, "sensor_health": "DEGRADED", "temperature": 8.0, "ambient_temperature": 38.0}
    print("Health Engine Test Result:", calculate_container_health(t))
