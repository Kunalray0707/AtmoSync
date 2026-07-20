"""
AtmoSync Route Tracking & Live Map API Route
"""

from fastapi import APIRouter
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.spoilage_engine import calculate_spoilage_metrics

router = APIRouter(prefix="/api/routes", tags=["Route Tracking"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("", summary="Get live GPS tracking and route trajectory points for map overlay")
def get_route_tracking():
    snapshot = fleet.generate_fleet_snapshot()
    locations = []

    for item in snapshot:
        spoilage = calculate_spoilage_metrics(item)
        locations.append({
            "container_id": item["container_id"],
            "shipment_id": item["shipment_id"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "commodity": item["commodity"],
            "temperature": item["temperature"],
            "spoilage_risk_score_pct": spoilage["spoilage_risk_score_pct"],
            "origin": item["origin"],
            "destination": item["destination"],
            "remaining_distance_km": item["remaining_distance_km"],
            "gps_speed": item["gps_speed"]
        })

    return {"active_shipments_map_data": locations}
