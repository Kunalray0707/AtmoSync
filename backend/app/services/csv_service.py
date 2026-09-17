"""CSV processing service for bulk data imports."""

import csv
import io
from typing import Any, Dict, List, Tuple


def parse_sensor_csv(content: bytes) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Parse sensor CSV content into typed rows and validation errors."""
    required = {"truck_id", "commodity", "temperature", "humidity"}
    errors: List[str] = []
    rows: List[Dict[str, Any]] = []

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [], ["File must be UTF-8 encoded"]

    reader = csv.DictReader(io.StringIO(text))
    missing = sorted(required - set(reader.fieldnames or []))
    if missing:
        return [], [f"Missing required columns: {', '.join(missing)}"]

    numeric_fields = {
        "temperature": float,
        "humidity": float,
        "gps_lat": float,
        "gps_lon": float,
        "battery": float,
        "market_price": float,
        "quantity": float,
    }
    for line_number, raw_row in enumerate(reader, start=2):
        row = {
            key: value.strip() if isinstance(value, str) else value
            for key, value in raw_row.items()
        }
        try:
            for field, converter in numeric_fields.items():
                if row.get(field) in (None, ""):
                    row[field] = None
                else:
                    row[field] = converter(row[field])
            if row.get("door_status") not in (None, ""):
                row["door_status"] = str(row["door_status"]).lower() in {
                    "1", "true", "yes", "closed"
                }
            if not row["truck_id"] or not row["commodity"]:
                raise ValueError("truck_id and commodity are required")
            rows.append(row)
        except (TypeError, ValueError) as exc:
            errors.append(f"Row {line_number}: {exc}")

    return rows, errors
