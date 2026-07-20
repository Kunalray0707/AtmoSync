"""
AtmoSync Spoilage Analytics API Route
"""

from typing import Optional
from fastapi import APIRouter, Query
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.spoilage_engine import calculate_spoilage_metrics
from analytics.loss_estimator import calculate_financial_and_carbon_loss

router = APIRouter(prefix="/api/spoilage", tags=["Spoilage Analytics"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("", summary="Get fleet spoilage risk breakdown and thermal degradation metrics")
def get_spoilage_analytics(
    min_risk: Optional[float] = Query(0.0, ge=0.0, le=100.0, description="Filter minimum spoilage risk %")
):
    snapshot = fleet.generate_fleet_snapshot()
    results = []
    high_risk_count = 0

    for item in snapshot:
        spoilage = calculate_spoilage_metrics(item)
        loss = calculate_financial_and_carbon_loss(item)
        combined = {**item, "spoilage": spoilage, "loss": loss}

        if spoilage["spoilage_risk_score_pct"] >= 50.0:
            high_risk_count += 1

        if spoilage["spoilage_risk_score_pct"] >= min_risk:
            results.append(combined)

    return {
        "total_containers_evaluated": len(snapshot),
        "high_spoilage_risk_count": high_risk_count,
        "containers": results
    }
