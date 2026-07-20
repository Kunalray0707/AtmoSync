"""
AtmoSync Kafka Event Schemas & Validation Models
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class TelemetryEventSchema(BaseModel):
    timestamp: str
    container_id: str = Field(..., description="Unique Container Identifier")
    shipment_id: str = Field(..., description="Unique Shipment Identifier")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    commodity: str
    temperature: float = Field(..., description="Container Micro-climate Temp (°C)")
    humidity: float = Field(..., ge=0.0, le=100.0)
    door_open: bool = False
    battery: float = Field(..., ge=0.0, le=100.0)
    gps_speed: float = Field(..., ge=0.0)
    ambient_temperature: float
    ambient_humidity: float
    weather_condition: str
    market_price: float = Field(..., gt=0.0)
    destination: str
    origin: str
    remaining_distance_km: float = Field(..., ge=0.0)
    estimated_arrival: str
    fuel_consumption_l_per_100km: float
    co2_emission_kg_hr: float
    sensor_health: str = "HEALTHY"
    alternative_destinations: Optional[List[Dict[str, Any]]] = []

    @field_validator("sensor_health")
    def validate_health(cls, v):
        allowed = {"HEALTHY", "DEGRADED", "MALFUNCTION", "CRITICAL"}
        if v.upper() not in allowed:
            return "HEALTHY"
        return v.upper()


class AlertEventSchema(BaseModel):
    alert_id: str
    timestamp: str
    container_id: str
    shipment_id: str
    severity: str  # INFO, WARNING, CRITICAL
    alert_type: str  # TEMP_EXCURSION, SPOILAGE_RISK, DOOR_BREACH, BATTERY_LOW, ARBITRAGE_OPPORTUNITY
    message: str
    current_value: float
    threshold_value: float
    recommended_action: str


class DLQEventSchema(BaseModel):
    original_topic: str
    failed_event: Dict[str, Any]
    error_message: str
    failed_at: str
    retry_count: int = 0
