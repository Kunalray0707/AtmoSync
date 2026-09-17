"""Dataset-driven analytics primitives for the AtmoSync Streamlit dashboard."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from analytics.spoilage_engine import calculate_spoilage_metrics


ROLE_ALIASES: dict[str, tuple[str, ...]] = {
    "timestamp": ("timestamp", "datetime", "date", "time", "recorded_at", "event_at", "scheduled_delivery_date", "delivered_to_client_date", "delivery_recorded_date"),
    "quantity": ("quantity", "qty", "units", "volume", "count", "amount", "line_item_quantity"),
    "revenue": ("revenue", "sales", "sales_amount", "gross_sales", "turnover", "line_item_value"),
    "cost": ("cost", "expense", "cogs", "purchase_cost", "total_cost", "freight_cost_usd_clean", "cost_per_kg_usd"),
    "price": ("price", "unit_price", "sale_price", "market_price", "spot_price", "rate", "pack_price"),
    "risk": ("risk", "risk_score", "risk_level", "probability", "score"),
    "spoilage": ("spoilage", "spoiled", "decay", "waste"),
    "temperature": ("temperature", "temp", "temp_c", "celsius", "thermal"),
    "humidity": ("humidity", "rh", "relative_humidity", "moisture"),
    "gas": ("gas", "air_quality", "voc", "ethylene"),
    "co2": ("co2", "carbon_dioxide"),
    "pressure": ("pressure", "barometric"),
    "product": ("product", "product_name", "item", "item_name", "sku", "crop", "item_description", "molecule_test_type"),
    "commodity": ("commodity", "cargo", "produce", "fruit", "product_group", "sub_classification"),
    "supplier": ("supplier", "vendor", "seller", "manufacturing_site"),
    "customer": ("customer", "buyer", "recipient"),
    "location": ("location", "site", "region", "city", "country", "manufacturing_site"),
    "warehouse": ("warehouse", "depot", "storage"),
    "container": ("container", "container_id", "reefer", "truck_id", "asset_id"),
    "shipment": ("shipment", "shipment_id", "order", "delivery", "po_so", "asn_dn", "project_code"),
    "route": ("route", "origin", "destination"),
    "inventory": ("inventory", "stock", "on_hand", "available"),
}


def _normalized(value: object) -> str:
    return "".join(character for character in str(value).lower() if character.isalnum())


def _is_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


def detect_columns(frame: pd.DataFrame) -> dict[str, Any]:
    """Infer conservative semantic roles from names and compatible dtypes."""
    numeric = [str(column) for column in frame.columns if _is_numeric(frame[column])]
    categorical = [
        str(column)
        for column in frame.columns
        if not _is_numeric(frame[column]) and not pd.api.types.is_datetime64_any_dtype(frame[column])
    ]
    date_columns: list[str] = []
    for column in frame.columns:
        series = frame[column]
        name = _normalized(column)
        if pd.api.types.is_datetime64_any_dtype(series) or any(_normalized(token) in name for token in ROLE_ALIASES["timestamp"]):
            parsed = pd.to_datetime(series, format="mixed", errors="coerce")
            if parsed.notna().mean() >= 0.6:
                date_columns.append(str(column))

    roles: dict[str, str | None] = {}
    used: set[str] = set()
    for role, aliases in ROLE_ALIASES.items():
        candidates: list[tuple[int, str]] = []
        for column in frame.columns:
            name = _normalized(column)
            alias_score = max((3 if name == _normalized(alias) else 2 if _normalized(alias) in name else 0 for alias in aliases), default=0)
            if alias_score == 0:
                continue
            if role in {"quantity", "revenue", "cost", "price", "risk", "spoilage", "temperature", "humidity", "gas", "co2", "pressure", "inventory"} and not _is_numeric(frame[column]):
                continue
            if role == "cost" and any(token in name for token in ("perkg", "perunit", "unitcost")):
                continue
            if role == "timestamp" and str(column) not in date_columns:
                continue
            if str(column) in used and role not in {"risk", "spoilage"}:
                continue
            candidates.append((alias_score, str(column)))
        if candidates:
            candidates.sort(key=lambda item: (-item[0], item[1]))
            roles[role] = candidates[0][1]
            if role not in {"risk", "spoilage"}:
                used.add(candidates[0][1])
        else:
            roles[role] = None

    identifiers = [
        str(column)
        for column in frame.columns
        if frame[column].nunique(dropna=True) < len(frame) and ("id" in _normalized(column) or _normalized(column) in {"sku", "code"})
    ]
    return {
        "roles": roles,
        "numeric": numeric,
        "categorical": categorical,
        "date": date_columns,
        "identifiers": identifiers,
    }


def normalize_dataset(frame: pd.DataFrame, columns: dict[str, Any]) -> pd.DataFrame:
    """Return a copy with detected timestamps parsed and blank rows removed."""
    normalized = frame.copy()
    timestamp = columns["roles"].get("timestamp")
    if timestamp:
        normalized[timestamp] = pd.to_datetime(normalized[timestamp], errors="coerce")
    return normalized.dropna(how="all").reset_index(drop=True)


def enrich_spoilage_risk(frame: pd.DataFrame, roles: dict[str, str | None]) -> tuple[pd.DataFrame, dict[str, str | None]]:
    """Apply the existing spoilage engine only when the dataset has its inputs."""
    temperature = roles.get("temperature")
    humidity = roles.get("humidity")
    if not temperature or not humidity:
        return frame, roles
    enriched = frame.copy()
    commodity = roles.get("commodity")
    scores: list[float] = []
    categories: list[str] = []
    for _, row in enriched.iterrows():
        telemetry = {"temperature": row.get(temperature), "humidity": row.get(humidity)}
        if commodity:
            telemetry["commodity"] = row.get(commodity)
        try:
            result = calculate_spoilage_metrics(telemetry)
            scores.append(float(result["spoilage_risk_score_pct"]))
            categories.append(str(result["spoilage_category"]))
        except (TypeError, ValueError):
            scores.append(np.nan)
            categories.append("Unavailable")
    enriched["_atmosync_spoilage_risk"] = scores
    enriched["_atmosync_risk_category"] = categories
    updated_roles = dict(roles)
    updated_roles["risk"] = "_atmosync_spoilage_risk"
    return enriched, updated_roles


def profile_dataset(frame: pd.DataFrame) -> dict[str, Any]:
    missing = frame.isna().sum()
    columns = detect_columns(frame)
    return {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "duplicates": int(frame.duplicated().sum()),
        "missing": {str(key): int(value) for key, value in missing[missing > 0].items()},
        "dtypes": {str(name): str(dtype) for name, dtype in frame.dtypes.items()},
        "numeric_columns": columns["numeric"],
        "categorical_columns": columns["categorical"],
        "date_columns": columns["date"],
        "roles": columns["roles"],
    }


def _numeric(frame: pd.DataFrame, column: str | None) -> pd.Series | None:
    if not column or column not in frame.columns:
        return None
    values = pd.to_numeric(frame[column], errors="coerce").dropna()
    return values if not values.empty else None


def kpis(frame: pd.DataFrame, roles: dict[str, str | None]) -> dict[str, float | int]:
    """Compute only metrics backed by selected dataset columns."""
    result: dict[str, float | int] = {"Total records": int(len(frame))}
    aggregations = {
        "Total quantity": ("quantity", "sum"),
        "Total revenue": ("revenue", "sum"),
        "Total cost": ("cost", "sum"),
        "Average price": ("price", "mean"),
        "Average temperature": ("temperature", "mean"),
        "Average humidity": ("humidity", "mean"),
        "Average risk": ("risk", "mean"),
        "Total inventory": ("inventory", "sum"),
    }
    for label, (role, operation) in aggregations.items():
        values = _numeric(frame, roles.get(role))
        if values is not None:
            result[label] = round(float(getattr(values, operation)()), 3)

    if "Total revenue" in result and "Total cost" in result:
        result["Profit"] = round(float(result["Total revenue"]) - float(result["Total cost"]), 3)
        revenue = float(result["Total revenue"])
        result["Margin %"] = round((float(result["Profit"]) / revenue) * 100, 3) if revenue else 0.0
    risk_values = _numeric(frame, roles.get("risk"))
    if risk_values is not None:
        result["High-risk records"] = int((risk_values >= 50).sum())
    spoilage = roles.get("spoilage")
    if spoilage and spoilage in frame.columns:
        values = frame[spoilage]
        if _is_numeric(values):
            result["Spoilage rate %"] = round(float((pd.to_numeric(values, errors="coerce") > 0).mean() * 100), 3)
        else:
            result["Spoilage rate %"] = round(float(values.astype(str).str.lower().isin({"yes", "true", "spoiled", "1", "high"}).mean() * 100), 3)
    return result


def group_summary(frame: pd.DataFrame, group_column: str, value_column: str) -> pd.DataFrame:
    values = pd.to_numeric(frame[value_column], errors="coerce")
    grouped = frame.assign(_value=values).dropna(subset=[group_column, "_value"])
    if grouped.empty:
        return pd.DataFrame(columns=[group_column, value_column])
    return grouped.groupby(group_column, as_index=False)["_value"].sum().rename(columns={"_value": value_column}).sort_values(value_column, ascending=False)


def findings(frame: pd.DataFrame, roles: dict[str, str | None]) -> list[str]:
    messages: list[str] = []
    metrics = kpis(frame, roles)
    if "Total records" in metrics:
        messages.append(f"The selected dataset contains {metrics['Total records']:,} records across {len(frame.columns)} columns.")
    group_column = roles.get("product") or roles.get("commodity") or roles.get("location")
    quantity_column = roles.get("quantity")
    if group_column and quantity_column:
        summary = group_summary(frame, group_column, quantity_column)
        if not summary.empty:
            leader = summary.iloc[0]
            total = float(summary[quantity_column].sum())
            share = (float(leader[quantity_column]) / total * 100) if total else 0
            messages.append(f"{leader[group_column]} accounts for {share:.1f}% of recorded quantity.")
    if "High-risk records" in metrics:
        messages.append(f"{metrics['High-risk records']:,} records meet the configured high-risk threshold of 50.")
    timestamp = roles.get("timestamp")
    if timestamp and timestamp in frame.columns:
        dates = pd.to_datetime(frame[timestamp], errors="coerce").dropna()
        if len(dates) > 1:
            messages.append(f"The selected time range is {dates.min().date()} to {dates.max().date()}.")
    return messages


def alerts(frame: pd.DataFrame, roles: dict[str, str | None]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    risk = roles.get("risk")
    if risk:
        values = pd.to_numeric(frame[risk], errors="coerce")
        for index in frame.index[values >= 50]:
            rows.append({"Severity": "High", "Record": int(index), "Description": f"Risk score is {values.loc[index]:.2f}.", "Metric": risk})
    for role, label, threshold in (("temperature", "Temperature", None), ("humidity", "Humidity", None)):
        column = roles.get(role)
        if not column:
            continue
        values = pd.to_numeric(frame[column], errors="coerce")
        if role == "temperature":
            mask = (values < -50) | (values > 80)
        else:
            mask = (values < 0) | (values > 100)
        for index in frame.index[mask.fillna(False)]:
            rows.append({"Severity": "Critical", "Record": int(index), "Description": f"{label} value is outside the valid range.", "Metric": column})
    return pd.DataFrame(rows, columns=["Severity", "Record", "Description", "Metric"])


def correlation(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = frame.select_dtypes(include=[np.number])
    return numeric.corr().fillna(0) if numeric.shape[1] >= 2 else pd.DataFrame()
