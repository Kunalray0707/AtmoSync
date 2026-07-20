"""
AtmoSync Forecasting API Route
"""

from typing import Optional
from fastapi import APIRouter, Query
from ml.forecasting import forecasting_engine

router = APIRouter(prefix="/api/forecast", tags=["Forecasting"])


@router.get("/prices", summary="Get 7-day spot market commodity price trend forecast")
def get_price_forecast(base_price: float = Query(3.40, gt=0.0, description="Current spot price $/kg")):
    return {"forecast_days": 7, "price_trend": forecasting_engine.forecast_price_trend(base_price)}


@router.get("/delay", summary="Get ETA delay estimation for shipment route")
def get_delay_forecast(speed: float = 35.0, distance: float = 2500.0, weather: str = "Clear"):
    return forecasting_engine.predict_delay(speed, distance, weather)
