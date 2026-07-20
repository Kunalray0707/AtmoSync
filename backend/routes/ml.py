"""
AtmoSync Machine Learning API Route
"""

from typing import Dict, Any
from fastapi import APIRouter, Body
from ml.spoilage_model import spoilage_ml_model
from ml.explainability import get_feature_importance_explainability

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])


@router.get("/metrics", summary="Get model performance cross-validation metrics")
def get_ml_metrics():
    return {
        "model_name": "XGBoost Container Spoilage Predictor",
        "version": "v1.2-xgboost",
        "performance_metrics": spoilage_ml_model.metrics
    }


@router.post("/predict", summary="Predict container spoilage risk using trained ML pipeline")
def predict_spoilage(telemetry: Dict[str, Any] = Body(...)):
    return spoilage_ml_model.predict(telemetry)


@router.post("/shap", summary="Get SHAP feature importance explainability breakdown")
def get_shap_explanation(telemetry: Dict[str, Any] = Body(...)):
    return get_feature_importance_explainability(telemetry)
