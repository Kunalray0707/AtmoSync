"""Commodity request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CommodityCreate(BaseModel):
    name: str = Field(..., max_length=100)
    commodity_type: str = Field(..., max_length=50)
    unit: str = Field(default="kg", max_length=20)
    current_price: Optional[float] = Field(None, ge=0)
    region: Optional[str] = Field(None, max_length=100)
    season: Optional[str] = Field(None, max_length=50)
    spoilage_threshold_temp: Optional[float] = None
    spoilage_threshold_humidity: Optional[float] = Field(None, ge=0, le=100)
    shelf_life_days: Optional[int] = Field(None, ge=0)


class CommodityUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    commodity_type: Optional[str] = Field(None, max_length=50)
    current_price: Optional[float] = Field(None, ge=0)
    region: Optional[str] = Field(None, max_length=100)
    season: Optional[str] = Field(None, max_length=50)
    spoilage_threshold_temp: Optional[float] = None
    spoilage_threshold_humidity: Optional[float] = Field(None, ge=0, le=100)
    shelf_life_days: Optional[int] = Field(None, ge=0)


class CommodityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    commodity_type: str
    unit: str
    current_price: Optional[float] = None
    previous_price: Optional[float] = None
    price_change_pct: Optional[float] = None
    region: Optional[str] = None
    season: Optional[str] = None
    spoilage_threshold_temp: Optional[float] = None
    spoilage_threshold_humidity: Optional[float] = None
    shelf_life_days: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class DashboardSummary(BaseModel):
    total_commodities: int
    active_trucks: int
    total_alerts: int
    avg_spoilage_score: float
    avg_arbitrage_score: float
    total_sensor_readings: int