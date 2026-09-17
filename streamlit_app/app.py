"""AtmoSync operational dashboard."""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.api_client import ApiClient, ApiError
from streamlit_app.services.dataset import exports, load_dataset, profile_dataset

st.set_page_config(page_title="AtmoSync", page_icon="A", layout="wide")


def metric_row(summary: dict) -> None:
    columns = st.columns(4)
    metrics = [
        ("Commodities", summary.get("total_commodities", 0)),
        ("Active trucks", summary.get("active_trucks", 0)),
        ("Alerts", summary.get("total_alerts", 0)),
        ("Readings", summary.get("total_sensor_readings", 0)),
    ]
    for column, (label, value) in zip(columns, metrics):
        column.metric(label, value)


def api_page(client: ApiClient, title: str, endpoint: str, columns: list[str]) -> None:
    st.title(title)
    try:
        records = client.get(endpoint)
    except ApiError as exc:
        st.error(str(exc))
        st.info("Start the FastAPI backend and provide a valid bearer token in the sidebar.")
        return
    frame = pd.DataFrame(records)
    if frame.empty:
        st.info("The API returned no records.")
        return
    available = [column for column in columns if column in frame.columns]
    st.dataframe(frame[available], use_container_width=True, hide_index=True)


st.sidebar.title("AtmoSync")
token = st.sidebar.text_input("API token", type="password", help="Paste a bearer token from the API login response.")
page = st.sidebar.radio("Workspace", ["Overview", "Containers", "Alerts", "Dataset inspector"])
client = ApiClient(token or None)

if page == "Overview":
    st.title("Executive overview")
    try:
        summary = client.get("/commodities/dashboard/summary")
        metric_row(summary)
        chart_data = pd.DataFrame({"Metric": ["Spoilage risk", "Arbitrage score"], "Value": [summary.get("avg_spoilage_score", 0), summary.get("avg_arbitrage_score", 0)]})
        st.plotly_chart(px.bar(chart_data, x="Metric", y="Value", title="Average model scores"), use_container_width=True)
    except ApiError as exc:
        st.error(str(exc))
        st.info("The dashboard displays verified API data only; no offline production metrics are generated.")
elif page == "Containers":
    api_page(client, "Container monitoring", "/sensors/latest", ["truck_id", "commodity", "temperature", "humidity", "battery", "spoilage_score", "recorded_at"])
elif page == "Alerts":
    api_page(client, "Alerts center", "/alerts/", ["truck_id", "severity", "title", "message", "is_read", "created_at"])
else:
    st.title("Dataset inspector")
    uploaded = st.file_uploader("Upload a dataset", type=["csv", "xlsx", "xls", "parquet"])
    if uploaded:
        try:
            frame = load_dataset(uploaded.name, uploaded.getvalue())
            details = profile_dataset(frame)
            columns = st.columns(4)
            columns[0].metric("Rows", details["rows"])
            columns[1].metric("Columns", details["columns"])
            columns[2].metric("Duplicates", details["duplicates"])
            columns[3].metric("Missing fields", len(details["missing"]))
            st.dataframe(frame.head(100), use_container_width=True, hide_index=True)
            st.json({"dtypes": details["dtypes"], "missing": details["missing"]})
            csv_bytes, excel_bytes = exports(frame)
            st.download_button("Download CSV", csv_bytes, "atmosync-dataset.csv", "text/csv")
            st.download_button("Download Excel", excel_bytes, "atmosync-dataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except (ValueError, ImportError, OSError) as exc:
            st.error(f"Unable to inspect this file: {exc}")
    else:
        st.info("Upload a CSV, Excel, or Parquet file to inspect it locally.")