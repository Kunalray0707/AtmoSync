"""Dataset-driven AtmoSync analytics dashboard."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit_app.api_client import ApiClient, ApiError
from streamlit_app.services.analytics import (
    alerts,
    correlation,
    detect_columns,
    enrich_spoilage_risk,
    findings,
    group_summary,
    kpis,
    normalize_dataset,
)
from streamlit_app.services.dataset import DATA_DIR, discover_datasets, exports, load_dataset, load_local_dataset, profile_dataset, select_primary_dataset

st.set_page_config(page_title="AtmoSync Analytics", page_icon="A", layout="wide")
MAX_UPLOAD_BYTES = 250 * 1024 * 1024


@st.cache_data(show_spinner=False)
def load_uploaded_dataset(file_name: str, content: bytes) -> pd.DataFrame:
    return load_dataset(file_name, content)


def initialize_state() -> None:
    for key, value in {"dataset_name": None, "dataset": None, "uploaded_at": None, "dataset_source": None, "data_error": None}.items():
        st.session_state.setdefault(key, value)
    if st.session_state.dataset is None:
        primary = select_primary_dataset(discover_datasets())
        if primary:
            try:
                st.session_state.dataset = load_local_dataset(primary["path"])
                st.session_state.dataset_name = str(primary["name"])
                st.session_state.dataset_source = "local data directory"
                st.session_state.uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, ImportError, OSError) as exc:
                st.session_state.data_error = str(exc)


def money(value: float | int) -> str:
    return f"${float(value):,.2f}"


def show_onboarding() -> None:
    st.title("AtmoSync Analytics")
    st.subheader("Upload a dataset to begin analysis")
    st.write("Metrics, charts, risk scores, alerts, and reports are generated only from the selected dataset.")
    st.info(f"No dataset found. Add a dataset to {DATA_DIR} to begin analysis.")


def dataset_context(frame: pd.DataFrame, name: str, roles: dict[str, str | None]) -> None:
    st.caption(f"Dataset: {name} | Source: {st.session_state.dataset_source or 'uploaded session'} | Records: {len(frame):,} | Columns: {len(frame.columns)} | Refreshed: {st.session_state.uploaded_at or 'current session'}")
    active = [f"{role}: {column}" for role, column in roles.items() if column]
    st.caption("Detected fields: " + (", ".join(active) if active else "none"))


def render_kpis(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    values = kpis(frame, roles)
    items = list(values.items())
    for start in range(0, len(items), 4):
        columns = st.columns(min(4, len(items[start:start + 4])))
        for column, (label, value) in zip(columns, items[start:start + 4]):
            display = money(value) if any(word in label for word in ("revenue", "cost", "Profit", "loss")) else f"{value:,}" if isinstance(value, int) else f"{value:,.2f}"
            column.metric(label, display)


def render_dynamic_charts(frame: pd.DataFrame, info: dict[str, object]) -> None:
    numeric = list(info["numeric"])
    categorical = list(info["categorical"])
    dates = list(info["date"])
    st.subheader("Dynamic visualizations")
    if dates and numeric:
        date_column = dates[0]
        value_column = st.selectbox("Time-series measure", numeric, key="time_measure")
        series = frame[[date_column, value_column]].copy()
        series[date_column] = pd.to_datetime(series[date_column], errors="coerce")
        series[value_column] = pd.to_numeric(series[value_column], errors="coerce")
        series = series.dropna().sort_values(date_column)
        if not series.empty:
            trend = series.groupby(date_column, as_index=False)[value_column].mean()
            st.plotly_chart(px.line(trend, x=date_column, y=value_column, markers=True, title=f"{value_column} over time"), use_container_width=True)
    chart_columns = st.columns(2)
    if categorical and numeric:
        with chart_columns[0]:
            category = st.selectbox("Category breakdown", categorical, key="category_dimension")
            measure = st.selectbox("Category measure", numeric, key="category_measure")
            summary = group_summary(frame, category, measure).head(20)
            if not summary.empty:
                st.plotly_chart(px.bar(summary, x=category, y=measure, title=f"{measure} by {category}"), use_container_width=True)
    if len(numeric) >= 2:
        with chart_columns[1]:
            x_column = st.selectbox("X axis", numeric, key="scatter_x")
            y_options = [column for column in numeric if column != x_column] or numeric
            y_column = st.selectbox("Y axis", y_options, key="scatter_y")
            st.plotly_chart(px.scatter(frame, x=x_column, y=y_column, title=f"{y_column} vs {x_column}"), use_container_width=True)
    corr = correlation(frame)
    if not corr.empty:
        st.plotly_chart(px.imshow(corr, text_auto=True, aspect="auto", title="Numeric correlation"), use_container_width=True)


def page_upload() -> None:
    st.title("Dataset Upload")
    st.write("Load a real dataset into this session. No demo or fallback records are used.")
    local_sources = discover_datasets()
    if local_sources:
        st.subheader("Local data sources")
        source_names = [str(item["name"]) for item in local_sources]
        selected_name = st.selectbox("Select a discovered dataset", source_names)
        selected = next(item for item in local_sources if item["name"] == selected_name)
        st.caption(f"{selected_name} | {int(selected['bytes']):,} bytes | {DATA_DIR}")
        if st.button("Use selected local dataset"):
            st.session_state.dataset = load_local_dataset(selected["path"])
            st.session_state.dataset_name = selected_name
            st.session_state.dataset_source = "local data directory"
            st.session_state.uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("Dataset loaded successfully")
    st.subheader("Upload another dataset")
    uploaded = st.file_uploader("Drag and drop a dataset", type=["csv", "xlsx", "xls", "json", "parquet"], help="Maximum file size: 250 MB")
    if not uploaded:
        st.info("Supported formats: CSV, XLSX, JSON, and Parquet.")
        return
    if uploaded.size > MAX_UPLOAD_BYTES:
        st.error("This file exceeds the 250 MB upload limit.")
        return
    st.write({"file": uploaded.name, "bytes": uploaded.size, "type": uploaded.type or "unknown"})
    try:
        frame = load_uploaded_dataset(uploaded.name, uploaded.getvalue())
    except (ValueError, ImportError, OSError) as exc:
        st.error(f"Dataset validation failed: {exc}")
        return
    profile = profile_dataset(frame)
    st.success("Dataset loaded successfully")
    summary_columns = st.columns(4)
    summary_columns[0].metric("Rows", profile["rows"])
    summary_columns[1].metric("Columns", profile["columns"])
    summary_columns[2].metric("Duplicates", profile["duplicates"])
    summary_columns[3].metric("Missing fields", len(profile["missing"]))
    st.dataframe(frame.head(100), use_container_width=True, hide_index=True)
    with st.expander("Detected schema and quality", expanded=True):
        st.json({"dtypes": profile["dtypes"], "numeric": profile["numeric_columns"], "categorical": profile["categorical_columns"], "dates": profile["date_columns"], "roles": profile["roles"], "missing": profile["missing"]})
    if st.button("Use this dataset for dashboard", type="primary"):
        st.session_state.dataset_name = uploaded.name
        st.session_state.dataset = normalize_dataset(frame, detect_columns(frame))
        st.session_state.dataset_source = "uploaded session"
        st.session_state.uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("This dataset is now selected for dashboard analysis.")


def page_dashboard(frame: pd.DataFrame, name: str, info: dict[str, object], roles: dict[str, str | None]) -> None:
    st.title("Dashboard")
    dataset_context(frame, name, roles)
    render_kpis(frame, roles)
    render_dynamic_charts(frame, info)
    st.subheader("Data-backed findings")
    for message in findings(frame, roles):
        st.write(f"- {message}")


def page_explorer(frame: pd.DataFrame, name: str, info: dict[str, object], roles: dict[str, str | None]) -> None:
    st.title("Dataset Explorer")
    dataset_context(frame, name, roles)
    search = st.text_input("Search all text fields")
    selected_columns = st.multiselect("Columns", list(frame.columns), default=list(frame.columns))
    filtered = frame[selected_columns].copy() if selected_columns else frame.iloc[:, 0:0].copy()
    if search and not filtered.empty:
        mask = filtered.astype(str).apply(lambda column: column.str.contains(search, case=False, na=False)).any(axis=1)
        filtered = filtered[mask]
    if selected_columns and info["categorical"]:
        options_columns = [column for column in info["categorical"] if column in selected_columns]
        if options_columns:
            filter_column = st.selectbox("Optional category filter", ["None"] + options_columns)
            if filter_column != "None":
                options = sorted(filtered[filter_column].dropna().astype(str).unique().tolist())
                chosen = st.multiselect(f"Values in {filter_column}", options)
                if chosen:
                    filtered = filtered[filtered[filter_column].astype(str).isin(chosen)]
    st.caption(f"Showing {len(filtered):,} of {len(frame):,} records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("Download filtered dataset", filtered.to_csv(index=False).encode("utf-8"), "atmosync-filtered.csv", "text/csv")
    with st.expander("Descriptive statistics"):
        st.dataframe(filtered.describe(include="all").transpose(), use_container_width=True)
    with st.expander("Unique values"):
        st.dataframe(pd.DataFrame({"column": filtered.columns, "unique_values": [filtered[column].nunique(dropna=True) for column in filtered.columns]}), use_container_width=True, hide_index=True)


def page_sales(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Sales & Inventory")
    revenue, cost = roles.get("revenue"), roles.get("cost")
    if not any((revenue, cost, roles.get("quantity"), roles.get("price"), roles.get("inventory"))):
        st.info("Sales analysis requires a revenue, cost, quantity, price, or inventory column.")
        return
    render_kpis(frame, roles)
    group = roles.get("product") or roles.get("commodity") or roles.get("location")
    if group and revenue:
        st.plotly_chart(px.bar(group_summary(frame, group, revenue).head(20), x=group, y=revenue, title=f"Revenue by {group}"), use_container_width=True)
    if revenue and cost:
        business = frame[[revenue, cost]].apply(pd.to_numeric, errors="coerce").dropna().rename(columns={revenue: "Revenue", cost: "Cost"})
        business["Profit"] = business["Revenue"] - business["Cost"]
        st.dataframe(business.describe().transpose(), use_container_width=True)


def page_supply_chain(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Supply Chain")
    dimensions = [roles.get(key) for key in ("supplier", "customer", "location", "warehouse", "container", "shipment", "route", "product", "commodity")]
    dimensions = [column for column in dimensions if column and column in frame.columns]
    if not dimensions:
        st.info("Supply-chain analysis requires supplier, customer, location, warehouse, shipment, route, container, product, or commodity fields.")
        return
    for dimension in dimensions:
        st.subheader(dimension)
        st.dataframe(frame[dimension].value_counts(dropna=False).head(20).rename("records").reset_index(), use_container_width=True, hide_index=True)


def page_products(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Product & Commodity Analytics")
    dimensions = [roles.get("product"), roles.get("commodity")]
    dimensions = [column for column in dimensions if column and column in frame.columns]
    if not dimensions:
        st.info("Product analytics requires product, item, commodity, category, or product-group fields.")
        return
    measure = roles.get("revenue") or roles.get("quantity") or roles.get("price")
    for dimension in dimensions:
        st.subheader(dimension)
        if measure:
            summary = group_summary(frame, dimension, measure)
            if not summary.empty:
                columns = st.columns(2)
                with columns[0]:
                    st.plotly_chart(px.bar(summary.head(20), x=dimension, y=measure, title=f"Top {dimension} by {measure}"), use_container_width=True)
                with columns[1]:
                    st.dataframe(summary.head(20), use_container_width=True, hide_index=True)
        else:
            st.dataframe(frame[dimension].value_counts().head(20).rename("records").reset_index(), use_container_width=True, hide_index=True)


def page_data_quality(frame: pd.DataFrame) -> None:
    st.title("Data Quality")
    missing = frame.isna().sum().rename("missing_values").to_frame()
    missing["missing_percent"] = (missing["missing_values"] / max(1, len(frame)) * 100).round(2)
    missing = missing.sort_values("missing_values", ascending=False)
    columns = st.columns(4)
    columns[0].metric("Rows", len(frame))
    columns[1].metric("Columns", len(frame.columns))
    columns[2].metric("Duplicate rows", int(frame.duplicated().sum()))
    columns[3].metric("Missing cells", int(frame.isna().sum().sum()))
    st.dataframe(missing, use_container_width=True)
    st.plotly_chart(px.bar(missing.reset_index().head(20), x="index", y="missing_percent", title="Missing values by column"), use_container_width=True)
    st.dataframe(pd.DataFrame({"column": frame.columns, "dtype": [str(frame[column].dtype) for column in frame.columns], "unique_values": [frame[column].nunique(dropna=True) for column in frame.columns]}), use_container_width=True, hide_index=True)


def page_financial(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Financial & Opportunity Analytics")
    revenue, cost, price = roles.get("revenue"), roles.get("cost"), roles.get("price")
    if not revenue and not cost and not price:
        st.info("Financial analysis requires revenue, cost, price, or compatible value fields in the dataset.")
        return
    render_kpis(frame, roles)
    if revenue and cost:
        st.info(f"Profit is calculated as detected revenue minus detected cost: {revenue} - {cost}.")
    if price and roles.get("product"):
        summary = frame.assign(_price=pd.to_numeric(frame[price], errors="coerce")).groupby(roles["product"], as_index=False)["_price"].mean().sort_values("_price", ascending=False).head(20)
        st.plotly_chart(px.bar(summary, x=roles["product"], y="_price", title=f"Average {price} by product"), use_container_width=True)
    if not roles.get("temperature") or not roles.get("humidity"):
        st.info("Loss and arbitrage analysis requires compatible temperature and humidity fields; those fields are not present in the selected SCMS dataset.")


def page_sensors(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Sensor Monitoring")
    sensor_roles = [roles.get(key) for key in ("temperature", "humidity", "gas", "co2", "pressure")]
    sensor_roles = [column for column in sensor_roles if column and column in frame.columns]
    if not sensor_roles:
        st.info("Sensor monitoring requires temperature, humidity, gas, CO2, or pressure columns.")
        return
    st.dataframe(frame[sensor_roles].apply(pd.to_numeric, errors="coerce").describe().transpose()[["count", "mean", "min", "max"]], use_container_width=True)
    date_column = roles.get("timestamp")
    if date_column:
        sensor_frame = frame[[date_column] + sensor_roles].copy()
        sensor_frame[date_column] = pd.to_datetime(sensor_frame[date_column], errors="coerce")
        sensor_frame = sensor_frame.dropna(subset=[date_column]).sort_values(date_column)
        if not sensor_frame.empty:
            selected = st.selectbox("Sensor trend", sensor_roles)
            st.plotly_chart(px.line(sensor_frame, x=date_column, y=selected, title=f"{selected} over time"), use_container_width=True)
    sensor_alerts = alerts(frame, roles)
    if not sensor_alerts.empty:
        st.subheader("Threshold violations")
        st.dataframe(sensor_alerts, use_container_width=True, hide_index=True)


def page_risk(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Spoilage & Risk")
    risk = roles.get("risk")
    if not risk:
        st.info("Risk analysis requires a risk score column or both temperature and humidity columns for the existing spoilage engine.")
        return
    values = pd.to_numeric(frame[risk], errors="coerce")
    risk_frame = frame.assign(_risk=values).dropna(subset=["_risk"])
    if risk_frame.empty:
        st.info("The detected risk column contains no numeric values.")
        return
    st.plotly_chart(px.histogram(risk_frame, x="_risk", nbins=20, title="Risk score distribution"), use_container_width=True)
    category = roles.get("commodity") or roles.get("product") or roles.get("container")
    if category:
        summary = risk_frame.groupby(category, as_index=False)["_risk"].mean().sort_values("_risk", ascending=False).head(20)
        st.plotly_chart(px.bar(summary, x=category, y="_risk", title=f"Average risk by {category}"), use_container_width=True)
    high = risk_frame[risk_frame["_risk"] >= 50].drop(columns=["_risk"])
    st.subheader(f"High-risk records ({len(high):,})")
    st.dataframe(high.head(200), use_container_width=True, hide_index=True)


def page_insights(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("AI Insights")
    st.write("These are deterministic, data-backed findings from the selected dataset. No LLM credentials are configured in this dashboard.")
    for message in findings(frame, roles):
        st.write(f"- {message}")
    st.subheader("Recommendations")
    metrics = kpis(frame, roles)
    if metrics.get("High-risk records", 0):
        st.warning("Prioritize review of high-risk records and inspect the contributing sensor or risk columns.")
    if metrics.get("Spoilage rate %", 0) > 0:
        st.warning("Investigate records marked as spoiled and compare them with temperature, humidity, commodity, and location fields.")
    if not metrics.get("High-risk records") and not metrics.get("Spoilage rate %"):
        st.info("No risk or spoilage recommendation can be generated until those fields are present.")


def page_alerts(frame: pd.DataFrame, roles: dict[str, str | None]) -> None:
    st.title("Alert Center")
    generated = alerts(frame, roles)
    if generated.empty:
        st.success("No data-backed alerts were detected in the selected dataset.")
        return
    severity = st.multiselect("Severity", sorted(generated["Severity"].unique()), default=sorted(generated["Severity"].unique()))
    st.dataframe(generated[generated["Severity"].isin(severity)], use_container_width=True, hide_index=True)


def page_reports(frame: pd.DataFrame, name: str, roles: dict[str, str | None]) -> None:
    st.title("Reports")
    metrics = kpis(frame, roles)
    alert_frame = alerts(frame, roles)
    summary = {"dataset": name, "generated_at": datetime.now().isoformat(), "kpis": metrics, "roles": roles, "alerts": int(len(alert_frame))}
    st.download_button("Download dataset CSV", frame.to_csv(index=False).encode("utf-8"), "atmosync-dataset.csv", "text/csv")
    st.download_button("Download dataset JSON", frame.to_json(orient="records", date_format="iso").encode("utf-8"), "atmosync-dataset.json", "application/json")
    st.download_button("Download KPI summary", json.dumps(summary, indent=2, default=str).encode("utf-8"), "atmosync-summary.json", "application/json")
    st.download_button("Download alert report", alert_frame.to_csv(index=False).encode("utf-8"), "atmosync-alerts.csv", "text/csv")
    _, excel_bytes = exports(frame)
    st.download_button("Download Excel workbook", excel_bytes, "atmosync-dataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def apply_global_filters(frame: pd.DataFrame, roles: dict[str, str | None]) -> tuple[pd.DataFrame, int]:
    """Apply sidebar filters before every dataset-driven page renders."""
    filtered = frame.copy()
    active = 0
    timestamp = roles.get("timestamp")
    if timestamp and timestamp in filtered.columns:
        dates = pd.to_datetime(filtered[timestamp], errors="coerce").dropna()
        if not dates.empty:
            selected = st.sidebar.date_input("Date range", value=(dates.min().date(), dates.max().date()), key="global_date_range")
            if isinstance(selected, tuple) and len(selected) == 2:
                start, end = pd.Timestamp(selected[0]), pd.Timestamp(selected[1]) + pd.Timedelta(days=1)
                parsed = pd.to_datetime(filtered[timestamp], errors="coerce")
                filtered = filtered[(parsed >= start) & (parsed < end)]
                if selected != (dates.min().date(), dates.max().date()):
                    active += 1
    for role, label in (("product", "Product"), ("commodity", "Commodity"), ("location", "Location"), ("supplier", "Supplier"), ("container", "Container")):
        column = roles.get(role)
        if not column or column not in filtered.columns:
            continue
        options = sorted(filtered[column].dropna().astype(str).unique().tolist())
        if len(options) > 1 and len(options) <= 200:
            selected = st.sidebar.multiselect(label, options, key=f"global_{role}")
            if selected:
                filtered = filtered[filtered[column].astype(str).isin(selected)]
                active += 1
    st.sidebar.caption(f"Active filters: {active}")
    return filtered, active


def page_live_operations() -> None:
    st.title("Live Operations")
    st.caption("This view uses the existing FastAPI simulator/API. Dataset analytics remain in the selected-dataset pages.")
    client = ApiClient()
    try:
        summary = client.get("/dashboard/summary")
        columns = st.columns(4)
        columns[0].metric("Active containers", summary.get("active_containers", 0))
        columns[1].metric("High-risk containers", summary.get("high_spoilage_risk_containers", 0))
        columns[2].metric("Cargo valuation", money(summary.get("total_cargo_valuation_usd", 0)))
        columns[3].metric("Projected loss", money(summary.get("total_projected_financial_loss_usd", 0)))
        st.dataframe(pd.DataFrame(client.get("/containers").get("containers", [])), use_container_width=True, hide_index=True)
    except ApiError as exc:
        st.error(str(exc))
        st.info("Start FastAPI with: .\\venv\\Scripts\\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000")


def main() -> None:
    initialize_state()
    st.sidebar.title("AtmoSync")
    st.sidebar.caption("Dataset-driven supply-chain intelligence")
    has_dataset = st.session_state.dataset is not None
    pages = ["Dashboard", "Dataset Upload", "Dataset Explorer", "Sales & Inventory", "Product & Commodity", "Supply Chain", "Sensor Monitoring", "Spoilage & Risk", "Financial & Opportunity", "Data Quality", "AI Insights", "Alerts", "Reports", "Live Operations"]
    page = st.sidebar.radio("Workspace", pages)
    if not has_dataset and page not in {"Dataset Upload", "Live Operations"}:
        show_onboarding()
        return
    if page == "Dataset Upload":
        page_upload()
        return
    if page == "Live Operations":
        page_live_operations()
        return
    frame = st.session_state.dataset.copy()
    name = str(st.session_state.dataset_name)
    info = detect_columns(frame)
    frame, _ = apply_global_filters(frame, info["roles"])
    frame, roles = enrich_spoilage_risk(frame, info["roles"])
    if page == "Dashboard":
        page_dashboard(frame, name, info, roles)
    elif page == "Dataset Explorer":
        page_explorer(frame, name, info, roles)
    elif page == "Sales & Inventory":
        page_sales(frame, roles)
    elif page == "Product & Commodity":
        page_products(frame, roles)
    elif page == "Supply Chain":
        page_supply_chain(frame, roles)
    elif page == "Sensor Monitoring":
        page_sensors(frame, roles)
    elif page == "Spoilage & Risk":
        page_risk(frame, roles)
    elif page == "Financial & Opportunity":
        page_financial(frame, roles)
    elif page == "Data Quality":
        page_data_quality(frame)
    elif page == "AI Insights":
        page_insights(frame, roles)
    elif page == "Alerts":
        page_alerts(frame, roles)
    else:
        page_reports(frame, name, roles)


main()
