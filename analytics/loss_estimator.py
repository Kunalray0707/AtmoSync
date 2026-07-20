"""
AtmoSync Financial Loss Estimator & Carbon Accounting Module
Calculates financial risk, product value degradation, cargo loss, and carbon tax impact.
"""

from typing import Dict, Any
from analytics.spoilage_engine import calculate_spoilage_metrics

CARGO_FULL_VALUATION = {
    "Avocados": 68000.0,    # USD per reefer load (20 metric tons)
    "Strawberries": 116000.0,
    "Bananas": 32000.0,
    "Blueberries": 144000.0,
    "Table Grapes": 58000.0,
    "Leafy Greens": 82000.0
}

CARBON_TAX_PER_TON_CO2 = 85.00  # USD per metric ton CO2 emitted


def calculate_financial_and_carbon_loss(telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes financial degradation loss, carbon emission footprint, and carbon tax penalties.
    """
    spoilage = calculate_spoilage_metrics(telemetry)
    commodity = telemetry.get("commodity", "Avocados")
    
    total_cargo_value = CARGO_FULL_VALUATION.get(commodity, 60000.0)
    spoilage_risk_pct = float(spoilage["spoilage_risk_score_pct"])
    freshness_pct = float(spoilage["freshness_index_pct"])
    
    # Financial Degradation Loss ($)
    quality_loss_factor = max(0.0, (100.0 - freshness_pct) / 100.0)
    financial_loss_usd = round(total_cargo_value * (quality_loss_factor ** 1.3), 2)
    
    # Total Salvage Value ($)
    estimated_salvage_value_usd = round(total_cargo_value - financial_loss_usd, 2)
    
    # Carbon & Fuel Accounting
    co2_kg_hr = float(telemetry.get("co2_emission_kg_hr", 14.5))
    remaining_dist_km = float(telemetry.get("remaining_distance_km", 1000.0))
    speed_kmh = max(10.0, float(telemetry.get("gps_speed", 35.0)))
    
    transit_hours_remaining = remaining_dist_km / speed_kmh
    projected_co2_kg = co2_kg_hr * transit_hours_remaining
    projected_co2_tons = projected_co2_kg / 1000.0
    
    carbon_tax_cost_usd = round(projected_co2_tons * CARBON_TAX_PER_TON_CO2, 2)
    
    return {
        "container_id": telemetry.get("container_id"),
        "commodity": commodity,
        "initial_cargo_valuation_usd": total_cargo_value,
        "spoilage_risk_score_pct": spoilage_risk_pct,
        "financial_loss_usd": financial_loss_usd,
        "estimated_salvage_value_usd": estimated_salvage_value_usd,
        "projected_co2_emission_kg": round(projected_co2_kg, 1),
        "projected_co2_tons": round(projected_co2_tons, 3),
        "carbon_tax_liability_usd": carbon_tax_cost_usd
    }


if __name__ == "__main__":
    event = {"container_id": "CONT-1003", "commodity": "Blueberries", "temperature": 8.0, "humidity": 70.0}
    loss_res = calculate_financial_and_carbon_loss(event)
    print("Loss Estimator Test Result:", loss_res)
