"""IoT Sensor Data model for real-time monitoring."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    truck_id = Column(String(50), nullable=False, index=True)
    commodity = Column(String(100), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    gps_lat = Column(Float, nullable=True)
    gps_lon = Column(Float, nullable=True)
    battery = Column(Float, nullable=True)
    door_status = Column(Boolean, default=True)  # True = closed, False = open
    market_price = Column(Float, nullable=True)
    quantity = Column(Float, nullable=True)
    weather_condition = Column(String(100), nullable=True)
    spoilage_score = Column(Float, nullable=True)
    arbitrage_score = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="sensor_data")

    def __repr__(self):
        return f"<SensorData {self.truck_id} - {self.commodity} @ {self.recorded_at}>"

