"""
AtmoSync Arbitrage & Rerouting API Route
"""

from fastapi import APIRouter
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.arbitrage_engine import evaluate_arbitrage_opportunity

router = APIRouter(prefix="/api/arbitrage", tags=["Arbitrage & Rerouting"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("", summary="Get all current profitable arbitrage rerouting opportunities")
def get_arbitrage_opportunities():
    snapshot = fleet.generate_fleet_snapshot()
    opportunities = []
    total_potential_profit_delta = 0.0

    for item in snapshot:
        arb = evaluate_arbitrage_opportunity(item)
        if arb["recommendation"] == "REROUTE_RECOMMENDED":
            opportunities.append(arb)
            total_potential_profit_delta += arb["max_net_profit_delta_usd"]

    return {
        "opportunities_count": len(opportunities),
        "total_potential_arbitrage_gain_usd": round(total_potential_profit_delta, 2),
        "opportunities": opportunities
    }


@router.get("/reroute", summary="Get top recommended route diversions for container fleet")
def get_top_reroutes():
    snapshot = fleet.generate_fleet_snapshot()
    reroutes = [evaluate_arbitrage_opportunity(item) for item in snapshot]
    reroutes.sort(key=lambda x: x["max_net_profit_delta_usd"], reverse=True)
    return {"rankings": reroutes[:10]}
