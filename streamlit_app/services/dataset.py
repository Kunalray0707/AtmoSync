"""Local dataset inspection used by the dashboard upload page."""

from io import BytesIO
from typing import Dict, Tuple

import pandas as pd


def load_dataset(file_name: str, content: bytes) -> pd.DataFrame:
    suffix = file_name.lower().rsplit(".", 1)[-1]
    if suffix == "csv":
        return pd.read_csv(BytesIO(content))
    if suffix in {"xlsx", "xls"}:
        return pd.read_excel(BytesIO(content))
    if suffix == "parquet":
        return pd.read_parquet(BytesIO(content))
    raise ValueError("Supported formats are CSV, Excel, and Parquet")


def profile_dataset(frame: pd.DataFrame) -> Dict[str, object]:
    missing = frame.isna().sum()
    return {
        "rows": len(frame),
        "columns": len(frame.columns),
        "duplicates": int(frame.duplicated().sum()),
        "missing": missing[missing > 0].to_dict(),
        "dtypes": {name: str(dtype) for name, dtype in frame.dtypes.items()},
    }


def exports(frame: pd.DataFrame) -> Tuple[bytes, bytes]:
    csv_bytes = frame.to_csv(index=False).encode("utf-8")
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name="dataset")
    return csv_bytes, buffer.getvalue()
