"""
AtmoSync Dynamic Dataset Inspection API Route
Allows uploading external CSV/Parquet files to auto-detect columns and adapt the pipeline schema.
"""

import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException
from ml.dataset_inspector import DynamicDatasetInspector

router = APIRouter(prefix="/api/inspect-dataset", tags=["Dataset Inspector"])


@router.post("", summary="Upload dataset CSV/Parquet for automatic column detection and adaptive schema mapping")
async def inspect_uploaded_dataset(file: UploadFile = File(...)):
    filename = file.filename
    contents = await file.read()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith(".parquet"):
            df = pd.read_parquet(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Only CSV and Parquet formats are supported.")

        inspector = DynamicDatasetInspector(df)
        inspection_result = inspector.inspect()
        adapted_df = inspector.adapt_to_standard_schema()

        return {
            "filename": filename,
            "status": "SUCCESS",
            "inspection": inspection_result,
            "adapted_sample_columns": list(adapted_df.columns),
            "adaptation_ready": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to inspect dataset: {str(e)}")
