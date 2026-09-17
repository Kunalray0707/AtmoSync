"""Alert model for notifications and warnings."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
import enum
from sqlalchemy import Enum as SAEnum


class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, enum.Enum):
    SPOILAGE = "spoilage"
    ARBITRAGE = "arbitrage"
    PRICE_DROP = "price_drop"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    DOOR_OPEN = "door_open"
    LOW_BATTERY = "low_battery"
    SYSTEM = "system"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    truck_id = Column(String(50), nullable=True)
    alert_type = Column(SAEnum(AlertType), nullable=False)
    severity = Column(SAEnum(AlertSeverity), default=AlertSeverity.INFO)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.severity}: {self.title}>"

