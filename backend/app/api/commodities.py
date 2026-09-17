"""Commodity catalog and dashboard summary endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.alert import Alert
from app.models.commodity import Commodity
from app.models.sensor_data import SensorData
from app.models.user import User
from app.schemas.commodity import (
    CommodityCreate,
    CommodityResponse,
    CommodityUpdate,
    DashboardSummary,
)

router = APIRouter(prefix="/commodities", tags=["Commodities"])


def _response(commodity: Commodity) -> CommodityResponse:
    return CommodityResponse(
        id=str(commodity.id),
        name=commodity.name,
        commodity_type=commodity.commodity_type,
        unit=commodity.unit,
        current_price=commodity.current_price,
        previous_price=commodity.previous_price,
        price_change_pct=commodity.price_change_pct,
        region=commodity.region,
        season=commodity.season,
        spoilage_threshold_temp=commodity.spoilage_threshold_temp,
        spoilage_threshold_humidity=commodity.spoilage_threshold_humidity,
        shelf_life_days=commodity.shelf_life_days,
        created_at=commodity.created_at,
        updated_at=commodity.updated_at,
    )


@router.get("/", response_model=List[CommodityResponse])
async def list_commodities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Commodity)
    if search:
        query = query.where(Commodity.name.ilike(f"%{search}%"))
    result = await db.execute(query.order_by(Commodity.name).offset(skip).limit(limit))
    return [_response(item) for item in result.scalars().all()]


@router.post("/", response_model=CommodityResponse, status_code=status.HTTP_201_CREATED)
async def create_commodity(
    data: CommodityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    commodity = Commodity(**data.model_dump())
    db.add(commodity)
    await db.flush()
    await db.refresh(commodity)
    return _response(commodity)


@router.get("/dashboard/summary", response_model=DashboardSummary)
async def dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    commodity_count = await db.scalar(select(func.count(Commodity.id)))
    truck_count = await db.scalar(select(func.count(func.distinct(SensorData.truck_id))))
    alert_count = await db.scalar(select(func.count(Alert.id)))
    reading_count = await db.scalar(select(func.count(SensorData.id)))
    spoilage = await db.scalar(select(func.avg(SensorData.spoilage_score)))
    arbitrage = await db.scalar(select(func.avg(SensorData.arbitrage_score)))
    return DashboardSummary(
        total_commodities=commodity_count or 0,
        active_trucks=truck_count or 0,
        total_alerts=alert_count or 0,
        avg_spoilage_score=round(spoilage or 0, 3),
        avg_arbitrage_score=round(arbitrage or 0, 3),
        total_sensor_readings=reading_count or 0,
    )


@router.get("/{commodity_id}", response_model=CommodityResponse)
async def get_commodity(
    commodity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    commodity = await db.get(Commodity, commodity_id)
    if commodity is None:
        raise HTTPException(status_code=404, detail="Commodity not found")
    return _response(commodity)


@router.put("/{commodity_id}", response_model=CommodityResponse)
async def update_commodity(
    commodity_id: str,
    data: CommodityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    commodity = await db.get(Commodity, commodity_id)
    if commodity is None:
        raise HTTPException(status_code=404, detail="Commodity not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(commodity, field, value)
    await db.flush()
    await db.refresh(commodity)
    return _response(commodity)


@router.delete("/{commodity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_commodity(
    commodity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    commodity = await db.get(Commodity, commodity_id)
    if commodity is None:
        raise HTTPException(status_code=404, detail="Commodity not found")
    await db.delete(commodity)