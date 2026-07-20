"""
Unit tests for SCMS Delivery History Dataset Cleaning & Analytics Engine
"""

from analytics.scms_analyzer import scms_analyzer


def test_scms_cleaning_and_summary():
    df_clean = scms_analyzer.clean_and_transform()
    assert len(df_clean) == 10324
    assert "Delivery_Delay_Days" in df_clean.columns
    assert "Freight_Cost_USD_Clean" in df_clean.columns

    summary = scms_analyzer.generate_analytics_summary()
    assert summary["total_shipments"] == 10324
    assert summary["total_line_item_value_usd"] > 1_000_000_000.0
    assert summary["on_time_delivery_pct"] > 80.0
    assert len(summary["top_destination_countries"]) > 0
