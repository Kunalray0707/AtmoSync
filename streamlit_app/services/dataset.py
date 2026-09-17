"""Local dataset inspection used by the dashboard upload page."""

from io import BytesIO
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd

from streamlit_app.services.analytics import ROLE_ALIASES, _normalized


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_dataset(file_name: str, content: bytes) -> pd.DataFrame:
    suffix = file_name.lower().rsplit(".", 1)[-1]
    if suffix == "csv":
        frame = pd.read_csv(BytesIO(content))
    elif suffix in {"xlsx", "xls"}:
        frame = pd.read_excel(BytesIO(content))
    elif suffix == "json":
        frame = pd.read_json(BytesIO(content))
    elif suffix == "parquet":
        frame = pd.read_parquet(BytesIO(content))
    else:
        raise ValueError("Supported formats are CSV, Excel, JSON, and Parquet")
    if frame.empty:
        raise ValueError("The uploaded dataset contains no rows")
    if len(frame.columns) == 0:
        raise ValueError("The uploaded dataset contains no columns")
    return frame


def discover_datasets(data_dir: Path = DATA_DIR) -> list[dict[str, object]]:
    """Discover supported local source files without modifying them."""
    if not data_dir.exists():
        return []
    datasets = []
    for path in sorted(data_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in {".csv", ".xlsx", ".xls", ".json", ".parquet"}:
            datasets.append({"name": path.name, "path": path, "bytes": path.stat().st_size})
    return datasets


def load_local_dataset(path: Path) -> pd.DataFrame:
    """Load a discovered source file through the same parser as uploads."""
    return load_dataset(path.name, path.read_bytes())


def select_primary_dataset(datasets: list[dict[str, object]]) -> dict[str, object] | None:
    """Prefer the project-produced cleaned SCMS dataset when present."""
    if not datasets:
        return None
    cleaned = [item for item in datasets if str(item["name"]).lower().endswith("_cleaned.csv")]
    return cleaned[0] if cleaned else datasets[0]


def profile_dataset(frame: pd.DataFrame) -> Dict[str, object]:
    missing = frame.isna().sum()
    numeric_columns = [str(column) for column in frame.columns if pd.api.types.is_numeric_dtype(frame[column])]
    date_candidates = []
    for column in frame.columns:
        name = _normalized(column)
        if not any(_normalized(token) in name for token in ROLE_ALIASES["timestamp"]):
            continue
        parsed = pd.to_datetime(frame[column], format="mixed", errors="coerce")
        if parsed.notna().mean() >= 0.6 and not pd.api.types.is_numeric_dtype(frame[column]):
            date_candidates.append(str(column))
    return {
        "rows": len(frame),
        "columns": len(frame.columns),
        "duplicates": int(frame.duplicated().sum()),
        "missing": missing[missing > 0].to_dict(),
        "dtypes": {name: str(dtype) for name, dtype in frame.dtypes.items()},
        "numeric_columns": numeric_columns,
        "date_columns": date_candidates,
        "invalid_numeric": {column: int(pd.to_numeric(frame[column], errors="coerce").isna().sum()) for column in numeric_columns},
    }


def exports(frame: pd.DataFrame) -> Tuple[bytes, bytes]:
    csv_bytes = frame.to_csv(index=False).encode("utf-8")
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name="dataset")
    return csv_bytes, buffer.getvalue()
