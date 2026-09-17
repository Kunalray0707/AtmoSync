"""Sensor data Pydantic schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SensorDataCreate(BaseModel):
    """Schema for creating sensor data."""
    truck_id: str = Field(..., max_length=50)
    commodity: str = Field(..., max_length=100)
    temperature: float = Field(..., ge=-50, le=100)
    humidity: float = Field(..., ge=0, le=100)
    gps_lat: Optional[float] = Field(None, ge=-90, le=90)
    gps_lon: Optional[float] = Field(None, ge=-180, le=180)
    battery: Optional[float] = Field(None, ge=0, le=100)
    door_status: Optional[bool] = True
    market_price: Optional[float] = Field(None, ge=0)
    quantity: Optional[float] = Field(None, ge=0)
    weather_condition: Optional[str] = None


class SensorDataResponse(BaseModel):
    """Schema for sensor data response."""
    id: str
    truck_id: str
    commodity: str
    temperature: float
    humidity: float
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    battery: Optional[float] = None
    door_status: bool
    market_price: Optional[float] = None
    quantity: Optional[float] = None
    weather_condition: Optional[str] = None
    spoilage_score: Optional[float] = None
    arbitrage_score: Optional[float] = None
    recorded_at: datetime

    class Config:
        from_attributes = True


class SensorDataFilter(BaseModel):
    """Schema for filtering sensor data."""
    truck_id: Optional[str] = None
    commodity: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_temp: Optional[float] = None
    max_temp: Optional[float] = None


class TruckLocation(BaseModel):
    """Schema for truck GPS location."""
    truck_id: str
    gps_lat: float
    gps_lon: float
    commodity: str
    temperature: float
    spoilage_score: Optional[float] = None
    recorded_at: datetime
