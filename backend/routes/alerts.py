"""
AtmoSync Alerts API Route
"""

from typing import Dict, Any
from fastapi import APIRouter, Body
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.spoilage_engine import calculate_spoilage_metrics
from backend.services.alert_service import alert_service

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("", summary="Get all active container alerts across the fleet")
def get_active_alerts():
    snapshot = fleet.generate_fleet_snapshot()
    alerts = []

    for item in snapshot:
        spoilage = calculate_spoilage_metrics(item)
        if item.get("door_open"):
            alerts.append({
                "alert_id": f"ALT-{item['container_id']}-DOOR",
                "container_id": item["container_id"],
                "shipment_id": item["shipment_id"],
                "severity": "CRITICAL",
                "alert_type": "DOOR_UNLATCHED",
                "message": f"Container door unlatched while transporting {item['commodity']}",
                "current_value": 1.0,
                "threshold_value": 0.0,
                "recommended_action": "Notify driver/crew immediately to inspect seal"
            })
        if spoilage["spoilage_risk_score_pct"] >= 50.0:
            alerts.append({
                "alert_id": f"ALT-{item['container_id']}-SPOILAGE",
                "container_id": item["container_id"],
                "shipment_id": item["shipment_id"],
                "severity": "HIGH",
                "alert_type": "SPOILAGE_RISK_EXCEEDED",
                "message": f"Spoilage risk reached {spoilage['spoilage_risk_score_pct']}% for {item['commodity']}",
                "current_value": spoilage["spoilage_risk_score_pct"],
                "threshold_value": 50.0,
                "recommended_action": "Evaluate rerouting or immediate spot market liquidation"
            })

    return {"count": len(alerts), "alerts": alerts}


@router.post("/trigger", summary="Manually trigger alert dispatch to Slack/Email")
def trigger_alert_dispatch(payload: Dict[str, Any] = Body(...)):
    res = alert_service.dispatch_alert(payload)
    return {"status": "SUCCESS", "dispatch_results": res}
