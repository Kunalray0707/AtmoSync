"""
Unit tests for Dynamic Dataset Inspector & Adaptive Schema Mapping
"""

import pandas as pd
from ml.dataset_inspector import DatasetInspector


def test_dataset_inspector_auto_detection():
    df = pd.DataFrame({
        "timestamp_utc": ["2026-07-20 10:00:00", "2026-07-20 10:01:00"],
        "REEFER_ID": ["CONT-801", "CONT-802"],
        "lat_coord": [51.95, 51.96],
        "lon_coord": [4.14, 4.15],
        "product_type": ["Avocados", "Blueberries"],
        "reefer_temp_celsius": [5.2, 8.4],
        "rel_humidity_pct": [85.0, 84.5],
        "spot_market_price": [3.40, 7.20]
    })

    inspector = DatasetInspector(df)
    res = inspector.profile()

    assert res["summary"]["row_count"] == 2
    assert res["summary"]["column_count"] == 8
    mappings = res["semantic_mapping"]
    assert mappings["container_id"] == "REEFER_ID"
    assert mappings["temperature"] == "reefer_temp_celsius"
    assert mappings["commodity"] == "product_type"

