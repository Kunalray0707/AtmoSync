"""
AtmoSync Dynamic Dataset Inspector & Semantic Schema Mapping Engine
Analyzes custom user-uploaded CSV / Parquet datasets, profiles columns, evaluates missingness,
detects telemetry semantics (temperature, humidity, timestamp, commodity, geolocation),
and generates dynamic data transformation mapping configurations.
"""

import os
import math
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


class DatasetInspector:
    """
    Automated Data Profiler & Adaptive Schema Mapping Engine.
    """

    SEMANTIC_KEYWORDS = {
        "timestamp": ["timestamp", "time", "date", "created_at", "datetime", "recorded_at"],
        "container_id": ["container_id", "container", "asset_id", "unit_id", "truck_id", "reefer_id"],
        "temperature": ["temp", "temperature", "temp_c", "celsius", "thermal", "ambient_temp"],
        "humidity": ["humidity", "rh", "relative_humidity", "moisture", "hum_pct"],
        "commodity": ["commodity", "product", "cargo", "item", "fruit", "produce", "crop"],
        "latitude": ["lat", "latitude", "origin_lat", "geo_lat", "location_lat"],
        "longitude": ["lon", "lng", "longitude", "origin_lon", "geo_lon", "location_lon"],
        "market_price": ["price", "market_price", "spot_price", "val", "unit_price", "rate"],
        "door_open": ["door_open", "door_status", "hatch_open", "breach"]
    }

    def __init__(self, file_path_or_df):
        if isinstance(file_path_or_df, str):
            self.file_path = file_path_or_df
            self.df = self._load_file(file_path_or_df)
        elif isinstance(file_path_or_df, pd.DataFrame):
            self.file_path = "DataFrame_In_Memory"
            self.df = file_path_or_df
        else:
            raise ValueError("Input must be a file path (str) or a pandas DataFrame.")

    def _load_file(self, path: str) -> pd.DataFrame:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.csv', '.txt']:
            return pd.read_csv(path)
        elif ext in ['.parquet', '.pq']:
            return pd.read_parquet(path)
        elif ext in ['.json', '.jsonl']:
            return pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def profile(self) -> Dict[str, Any]:
        """
        Executes comprehensive dataset profiling.
        """
        row_count, col_count = self.df.shape
        memory_usage_mb = round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        duplicate_rows = int(self.df.duplicated().sum())

        column_profiles = {}
        for col in self.df.columns:
            dtype_str = str(self.df[col].dtype)
            null_count = int(self.df[col].isnull().sum())
            null_pct = round((null_count / max(1, row_count)) * 100.0, 2)
            unique_count = int(self.df[col].nunique())

            stats = {}
            if pd.api.types.is_numeric_dtype(self.df[col]):
                clean_series = self.df[col].dropna()
                if not clean_series.empty:
                    stats = {
                        "min": float(clean_series.min()),
                        "max": float(clean_series.max()),
                        "mean": float(clean_series.mean()),
                        "std": float(clean_series.std()) if len(clean_series) > 1 else 0.0,
                        "median": float(clean_series.median())
                    }
            else:
                top_counts = self.df[col].value_counts().head(5).to_dict()
                stats = {"top_values": {str(k): int(v) for k, v in top_counts.items()}}

            column_profiles[col] = {
                "dtype": dtype_str,
                "null_count": null_count,
                "null_percent": null_pct,
                "unique_values": unique_count,
                "statistics": stats
            }

        # Infer Semantic Schema Mapping
        semantic_mapping = self.infer_semantic_schema()
        quality_alerts = self._generate_quality_alerts(column_profiles, semantic_mapping)

        return {
            "source_file": os.path.basename(self.file_path),
            "summary": {
                "row_count": row_count,
                "column_count": col_count,
                "memory_usage_mb": memory_usage_mb,
                "duplicate_rows": duplicate_rows
            },
            "columns": column_profiles,
            "semantic_mapping": semantic_mapping,
            "quality_alerts": quality_alerts,
            "correlation_matrix": self._compute_correlation_matrix()
        }

    def infer_semantic_schema(self) -> Dict[str, Optional[str]]:
        """
        Infers standard telemetry fields from dataset column names.
        """
        mapping = {}
        columns_lower = {col.lower(): col for col in self.df.columns}

        for semantic_role, keywords in self.SEMANTIC_KEYWORDS.items():
            matched_col = None
            for kw in keywords:
                for col_lower, original_col in columns_lower.items():
                    if kw == col_lower or kw in col_lower:
                        matched_col = original_col
                        break
                if matched_col:
                    break
            mapping[semantic_role] = matched_col

        return mapping

    def _compute_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Computes Pearson correlation for numeric columns.
        """
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty or numeric_df.shape[1] < 2:
            return {}
        
        corr = numeric_df.corr().fillna(0.0)
        corr_dict = {}
        for col1 in corr.columns:
            corr_dict[col1] = {col2: round(float(corr.loc[col1, col2]), 3) for col2 in corr.columns}
        return corr_dict

    def _generate_quality_alerts(self, column_profiles: Dict[str, Any], mapping: Dict[str, Any]) -> List[Dict[str, str]]:
        alerts = []
        # Missing essential telemetry mapping check
        critical_roles = ["timestamp", "container_id", "temperature", "commodity"]
        for role in critical_roles:
            if not mapping.get(role):
                alerts.append({
                    "severity": "WARNING",
                    "code": "MISSING_CRITICAL_ROLE",
                    "message": f"Could not automatically map critical semantic role '{role}'. Manual mapping recommended."
                })

        # High null percentage check
        for col, prof in column_profiles.items():
            if prof["null_percent"] > 20.0:
                alerts.append({
                    "severity": "HIGH",
                    "code": "HIGH_NULL_PERCENTAGE",
                    "message": f"Column '{col}' has {prof['null_percent']}% missing values."
                })

        # Out-of-bounds temperature check if temperature mapped
        temp_col = mapping.get("temperature")
        if temp_col and temp_col in column_profiles:
            stats = column_profiles[temp_col]["statistics"]
            if stats.get("min", 0) < -50 or stats.get("max", 0) > 80:
                alerts.append({
                    "severity": "CRITICAL",
                    "code": "EXTREME_TEMPERATURE_VALUES",
                    "message": f"Temperature column '{temp_col}' has out-of-range values: min {stats.get('min')}, max {stats.get('max')}."
                })

        return alerts


if __name__ == "__main__":
    sample_data = pd.DataFrame({
        "recorded_at": ["2026-07-20 10:00:00", "2026-07-20 10:01:00"],
        "reefer_id": ["CONT-100", "CONT-100"],
        "temp_c": [4.2, 8.9],
        "rh_pct": [85.0, 92.0],
        "cargo": ["Avocados", "Avocados"],
        "geo_lat": [25.7617, 25.7620],
        "geo_lon": [-80.1918, -80.1920]
    })
    inspector = DatasetInspector(sample_data)
    profile_result = inspector.profile()
    print("Dataset Inspector Profile Result:", profile_result)
