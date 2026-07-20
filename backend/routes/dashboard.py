"""
AtmoSync Dashboard Executive Summary API Route
"""

from fastapi import APIRouter
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.spoilage_engine import calculate_spoilage_metrics
from analytics.arbitrage_engine import evaluate_arbitrage_opportunity
from analytics.loss_estimator import calculate_financial_and_carbon_loss
from analytics.health_engine import calculate_container_health

router = APIRouter(prefix="/api/dashboard", tags=["Executive Dashboard"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("/summary", summary="Get high-level executive KPIs and overall cold-chain health")
def get_executive_summary():
    snapshot = fleet.generate_fleet_snapshot()

    total_containers = len(snapshot)
    high_spoilage_risk_count = 0
    total_cargo_valuation_usd = 0.0
    total_financial_loss_usd = 0.0
    total_arbitrage_opportunity_usd = 0.0
    total_co2_kg_hr = 0.0
    health_scores = []

    for item in snapshot:
        spoilage = calculate_spoilage_metrics(item)
        loss = calculate_financial_and_carbon_loss(item)
        arb = evaluate_arbitrage_opportunity(item)
        health = calculate_container_health(item)

        if spoilage["spoilage_risk_score_pct"] >= 50.0:
            high_spoilage_risk_count += 1

        total_cargo_valuation_usd += loss["initial_cargo_valuation_usd"]
        total_financial_loss_usd += loss["financial_loss_usd"]
        total_co2_kg_hr += float(item.get("co2_emission_kg_hr", 14.0))

        if arb["max_net_profit_delta_usd"] > 0:
            total_arbitrage_opportunity_usd += arb["max_net_profit_delta_usd"]

        health_scores.append(health["container_health_score_pct"])

    avg_health_score = round(sum(health_scores) / max(1, len(health_scores)), 1)

    return {
        "active_containers": total_containers,
        "high_spoilage_risk_containers": high_spoilage_risk_count,
        "fleet_container_health_index_pct": avg_health_score,
        "total_cargo_valuation_usd": round(total_cargo_valuation_usd, 2),
        "total_projected_financial_loss_usd": round(total_financial_loss_usd, 2),
        "identified_arbitrage_gain_usd": round(total_arbitrage_opportunity_usd, 2),
        "fleet_co2_emission_rate_kg_hr": round(total_co2_kg_hr, 1),
        "active_commodities_monitored": ["Avocados", "Strawberries", "Bananas", "Blueberries", "Table Grapes", "Leafy Greens"]
    }
