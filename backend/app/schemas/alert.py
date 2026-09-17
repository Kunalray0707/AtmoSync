"""Alert Pydantic schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertResponse(BaseModel):
    """Schema for alert response."""
    id: str
    truck_id: Optional[str] = None
    alert_type: str
    severity: str
    title: str
    message: str
    value: Optional[float] = None
    threshold: Optional[float] = None
    is_read: bool
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""
    is_read: Optional[bool] = None
    is_resolved: Optional[bool] = None
