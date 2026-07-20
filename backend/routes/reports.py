"""
AtmoSync Reports & Data Export API Route
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from simulator.iot_simulator import IoTTelemetryFleet
from analytics.spoilage_engine import calculate_spoilage_metrics
from backend.services.export_service import (
    generate_csv_report, generate_json_report,
    generate_excel_report, generate_pdf_report, generate_pptx_report
)

router = APIRouter(prefix="/api/reports", tags=["Reports & Export"])

fleet = IoTTelemetryFleet(fleet_size=20)


@router.get("/download", summary="Download executive reports in PDF, Excel, PPTX, CSV, or JSON format")
def download_report(
    format: str = Query("csv", description="Format: pdf | excel | pptx | csv | json")
):
    snapshot = fleet.generate_fleet_snapshot()
    processed_data = []

    for item in snapshot:
        spoilage = calculate_spoilage_metrics(item)
        processed_data.append({**item, **spoilage})

    fmt = format.lower()

    if fmt == "csv":
        buf = generate_csv_report(processed_data)
        return StreamingResponse(buf, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=atmosync_report.csv"})
    elif fmt == "json":
        buf = generate_json_report(processed_data)
        return StreamingResponse(buf, media_type="application/json", headers={"Content-Disposition": "attachment; filename=atmosync_report.json"})
    elif fmt in ["excel", "xlsx"]:
        buf = generate_excel_report(processed_data)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=atmosync_report.xlsx"})
    elif fmt == "pdf":
        summary = {"total_containers": len(processed_data), "high_risk_count": 3}
        buf = generate_pdf_report(summary, processed_data)
        return StreamingResponse(buf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=atmosync_executive_report.pdf"})
    elif fmt in ["pptx", "powerpoint"]:
        summary = {"total_containers": len(processed_data)}
        buf = generate_pptx_report(summary)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", headers={"Content-Disposition": "attachment; filename=atmosync_presentation.pptx"})
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Supported: pdf, excel, pptx, csv, json")
