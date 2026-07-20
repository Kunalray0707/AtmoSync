"""
AtmoSync Containers API Route
"""

from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.spoilage_engine import calculate_spoilage_metrics
from analytics.health_engine import calculate_container_health

router = APIRouter(prefix="/api/containers", tags=["Containers"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("", summary="Get all live active reefer containers")
def get_containers(
    commodity: Optional[str] = Query(None, description="Filter by commodity type"),
    status: Optional[str] = Query(None, description="Filter by sensor health status"),
    search: Optional[str] = Query(None, description="Search container or shipment ID")
):
    snapshot = fleet.generate_fleet_snapshot()
    results = []

    for item in snapshot:
        spoilage = calculate_spoilage_metrics(item)
        health = calculate_container_health(item)
        merged = {**item, **spoilage, **health}

        if commodity and merged["commodity"].lower() != commodity.lower():
            continue
        if status and merged["sensor_health"].lower() != status.lower():
            continue
        if search and (search.lower() not in merged["container_id"].lower() and search.lower() not in merged["shipment_id"].lower()):
            continue

        results.append(merged)

    return {"count": len(results), "containers": results}


@router.get("/{container_id}", summary="Get container detailed telemetry history and diagnostics")
def get_container_detail(container_id: str):
    snapshot = fleet.generate_fleet_snapshot()
    for item in snapshot:
        if item["container_id"].upper() == container_id.upper():
            spoilage = calculate_spoilage_metrics(item)
            health = calculate_container_health(item)
            return {**item, "spoilage_analytics": spoilage, "container_health": health}

    raise HTTPException(status_code=404, detail=f"Container {container_id} not found")
