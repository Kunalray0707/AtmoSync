"""Commodity model for agricultural product tracking."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    commodity_type = Column(String(50), nullable=False)
    unit = Column(String(20), nullable=False, default="kg")
    current_price = Column(Float, nullable=True)
    previous_price = Column(Float, nullable=True)
    price_change_pct = Column(Float, nullable=True)
    region = Column(String(100), nullable=True)
    season = Column(String(50), nullable=True)
    spoilage_threshold_temp = Column(Float, nullable=True)
    spoilage_threshold_humidity = Column(Float, nullable=True)
    shelf_life_days = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Commodity {self.name} ({self.commodity_type})>"

