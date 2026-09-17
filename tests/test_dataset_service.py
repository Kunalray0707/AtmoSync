from io import BytesIO

import pandas as pd
import pytest

from streamlit_app.services.analytics import alerts, detect_columns, enrich_spoilage_risk, kpis
from streamlit_app.services.dataset import discover_datasets, load_dataset, profile_dataset, select_primary_dataset


def test_csv_profile_reports_shape_duplicates_and_missing_values():
    frame = load_dataset("telemetry.csv", b"temperature,humidity\n5,90\n5,\n5,90\n")
    profile = profile_dataset(frame)

    assert profile["rows"] == 3
    assert profile["columns"] == 2
    assert profile["duplicates"] == 1
    assert profile["missing"] == {"humidity": 1}


def test_json_and_xlsx_datasets_load():
    frame = pd.DataFrame({"product": ["A", "B"], "quantity": [2, 3]})
    json_frame = load_dataset("sales.json", frame.to_json(orient="records").encode())
    assert json_frame.equals(frame)

    buffer = BytesIO()
    frame.to_excel(buffer, index=False)
    xlsx_frame = load_dataset("sales.xlsx", buffer.getvalue())
    assert xlsx_frame.equals(frame)


def test_empty_and_invalid_datasets_are_rejected():
    with pytest.raises(ValueError, match="no rows"):
        load_dataset("empty.csv", b"product,quantity\n")
    with pytest.raises(ValueError, match="Supported formats"):
        load_dataset("sales.txt", b"product\nA\n")


def test_dynamic_kpis_and_spoilage_are_dataset_dependent():
    frame = pd.DataFrame({
        "recorded_at": ["2026-01-01", "2026-01-02"],
        "product": ["A", "B"],
        "quantity": [10, 20],
        "revenue": [100, 300],
        "cost": [40, 100],
        "temperature": [5, 12],
        "humidity": [90, 70],
    })
    info = detect_columns(frame)
    enriched, roles = enrich_spoilage_risk(frame, info["roles"])
    metrics = kpis(enriched, roles)

    assert metrics["Total quantity"] == 30
    assert metrics["Total revenue"] == 400
    assert metrics["Profit"] == 260
    assert metrics["High-risk records"] == 1
    assert not alerts(enriched, roles).empty


def test_local_dataset_discovery_prefers_cleaned_source(tmp_path):
    (tmp_path / "scms_dataset.csv").write_text("id,value\n1,10\n", encoding="utf-8")
    (tmp_path / "scms_cleaned.csv").write_text("id,value\n1,10\n", encoding="utf-8")
    sources = discover_datasets(tmp_path)

    assert [source["name"] for source in sources] == ["scms_cleaned.csv", "scms_dataset.csv"]
    assert select_primary_dataset(sources)["name"] == "scms_cleaned.csv"