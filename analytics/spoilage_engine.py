"""
AtmoSync Spoilage & Thermal Kinetics Analytics Engine
Calculates Arrhenius Quality Decay, Remaining Shelf Life (RSL), Freshness Index, Thermal Drift, and Cold Chain Violations.
"""

import math
from typing import Dict, Any
from simulator.config import COMMODITIES

# Universal gas constant J / (mol * K)
R_GAS = 8.314


def calculate_spoilage_metrics(telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes scientific spoilage risk, remaining shelf life, freshness index, 
    and cold chain violation metrics for a given telemetry record.
    """
    commodity_name = telemetry.get("commodity", "Avocados")
    profile = COMMODITIES.get(commodity_name, COMMODITIES["Avocados"])
    
    current_temp = float(telemetry.get("temperature", 5.0))
    current_humidity = float(telemetry.get("humidity", 85.0))
    door_open = bool(telemetry.get("door_open", False))
    
    optimum_temp = profile["optimum_temp"]
    max_temp = profile["max_temp"]
    min_temp = profile["min_temp"]
    optimum_humidity = profile["optimum_humidity"]
    base_shelf_life = profile["base_shelf_life_days"]
    activation_energy = profile["activation_energy"]  # kJ/mol
    
    # 1. Temperature & Humidity Drift
    temp_drift = round(current_temp - optimum_temp, 2)
    humidity_drift = round(current_humidity - optimum_humidity, 2)
    
    # 2. Cold Chain Violation Detection
    is_temp_violation = current_temp > max_temp or current_temp < min_temp
    is_humidity_violation = abs(humidity_drift) > 10.0
    is_violation = is_temp_violation or is_humidity_violation or door_open
    
    # 3. Arrhenius Degradation Kinetics
    temp_k_opt = optimum_temp + 273.15
    temp_k_cur = current_temp + 273.15
    
    # Relative reaction rate relative to optimum temperature
    try:
        ea_j = activation_energy * 1000.0
        k_opt = math.exp(-ea_j / (R_GAS * temp_k_opt))
        k_cur = math.exp(-ea_j / (R_GAS * temp_k_cur))
        q_decay_ratio = k_cur / k_opt if k_opt > 0 else 1.0
    except Exception:
        q_decay_ratio = 1.0
        
    # Acceleration penalty for open door or extreme temperature spike
    if door_open:
        q_decay_ratio *= 1.8
    if current_temp > max_temp:
        q_decay_ratio *= (1.0 + 0.3 * (current_temp - max_temp))
        
    # 4. Remaining Shelf Life (RSL) calculation
    # Assume cargo is midway through shipment baseline progression
    estimated_days_passed = float(profile["base_shelf_life_days"]) * 0.35
    effective_days_used = estimated_days_passed * q_decay_ratio
    
    remaining_shelf_life_days = max(0.0, base_shelf_life - effective_days_used)
    remaining_shelf_life_hours = round(remaining_shelf_life_days * 24.0, 1)
    
    # 5. Freshness Index (0 - 100%)
    freshness_index = max(0.0, min(100.0, (remaining_shelf_life_days / base_shelf_life) * 100.0))
    spoilage_risk_score = round(100.0 - freshness_index, 2)
    freshness_index = round(freshness_index, 2)
    
    # Risk status classification
    if spoilage_risk_score >= 80.0:
        spoilage_category = "CRITICAL_SPOILAGE_RISK"
    elif spoilage_risk_score >= 50.0:
        spoilage_category = "HIGH_RISK"
    elif spoilage_risk_score >= 25.0:
        spoilage_category = "MODERATE_RISK"
    else:
        spoilage_category = "OPTIMAL_FRESHNESS"
        
    return {
        "container_id": telemetry.get("container_id"),
        "commodity": commodity_name,
        "temperature_celsius": current_temp,
        "temperature_drift_celsius": temp_drift,
        "humidity_percent": current_humidity,
        "humidity_drift_percent": humidity_drift,
        "arrhenius_decay_ratio": round(q_decay_ratio, 3),
        "remaining_shelf_life_days": round(remaining_shelf_life_days, 2),
        "remaining_shelf_life_hours": remaining_shelf_life_hours,
        "freshness_index_pct": freshness_index,
        "spoilage_risk_score_pct": spoilage_risk_score,
        "spoilage_category": spoilage_category,
        "is_cold_chain_violation": is_violation,
        "door_open_breach": door_open
    }


if __name__ == "__main__":
    test_telemetry = {
        "container_id": "CONT-1001",
        "commodity": "Strawberries",
        "temperature": 7.5,  # Excursion!
        "humidity": 88.0,
        "door_open": True
    }
    result = calculate_spoilage_metrics(test_telemetry)
    print("Spoilage Engine Test Result:", result)
