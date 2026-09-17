"""Sensor data API routes: CRUD, filtering, GPS tracking."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta, timezone

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.sensor_data import SensorData
from app.schemas.sensor import (
    SensorDataCreate,
    SensorDataResponse,
    SensorDataFilter,
    TruckLocation,
)

router = APIRouter(prefix="/sensors", tags=["Sensor Data"])


@router.post("/", response_model=SensorDataResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_reading(
    data: SensorDataCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new IoT sensor reading."""
    sensor_data = SensorData(
        user_id=current_user.id,
        truck_id=data.truck_id,
        commodity=data.commodity,
        temperature=data.temperature,
        humidity=data.humidity,
        gps_lat=data.gps_lat,
        gps_lon=data.gps_lon,
        battery=data.battery,
        door_status=data.door_status,
        market_price=data.market_price,
        quantity=data.quantity,
        weather_condition=data.weather_condition,
        spoilage_score=calculate_spoilage_score(data.temperature, data.humidity, data.commodity),
        recorded_at=datetime.now(timezone.utc),
    )
    db.add(sensor_data)
    await db.flush()
    await db.refresh(sensor_data)

    return SensorDataResponse(
        id=str(sensor_data.id),
        truck_id=sensor_data.truck_id,
        commodity=sensor_data.commodity,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity,
        gps_lat=sensor_data.gps_lat,
        gps_lon=sensor_data.gps_lon,
        battery=sensor_data.battery,
        door_status=sensor_data.door_status,
        market_price=sensor_data.market_price,
        quantity=sensor_data.quantity,
        weather_condition=sensor_data.weather_condition,
        spoilage_score=sensor_data.spoilage_score,
        arbitrage_score=sensor_data.arbitrage_score,
        recorded_at=sensor_data.recorded_at,
    )


@router.get("/", response_model=List[SensorDataResponse])
async def list_sensor_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    truck_id: Optional[str] = None,
    commodity: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List sensor data with optional filtering."""
    query = select(SensorData).where(SensorData.user_id == current_user.id)

    if truck_id:
        query = query.where(SensorData.truck_id == truck_id)
    if commodity:
        query = query.where(SensorData.commodity == commodity)
    if start_date:
        query = query.where(SensorData.recorded_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.where(SensorData.recorded_at <= datetime.fromisoformat(end_date))

    query = query.order_by(desc(SensorData.recorded_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    records = result.scalars().all()

    return [
        SensorDataResponse(
            id=str(r.id),
            truck_id=r.truck_id,
            commodity=r.commodity,
            temperature=r.temperature,
            humidity=r.humidity,
            gps_lat=r.gps_lat,
            gps_lon=r.gps_lon,
            battery=r.battery,
            door_status=r.door_status,
            market_price=r.market_price,
            quantity=r.quantity,
            weather_condition=r.weather_condition,
            spoilage_score=r.spoilage_score,
            arbitrage_score=r.arbitrage_score,
            recorded_at=r.recorded_at,
        )
        for r in records
    ]


@router.get("/latest", response_model=List[SensorDataResponse])
async def get_latest_readings(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the most recent sensor readings."""
    # Subquery to get latest reading per truck_id
    latest_ids = (
        select(
            SensorData.id,
            func.row_number().over(
                partition_by=SensorData.truck_id,
                order_by=desc(SensorData.recorded_at),
            ).label("rn"),
        )
        .where(SensorData.user_id == current_user.id)
        .subquery()
    )

    query = (
        select(SensorData)
        .where(SensorData.user_id == current_user.id, SensorData.id.in_(
            select(latest_ids.c.id).where(latest_ids.c.rn == 1)
        ))
        .order_by(desc(SensorData.recorded_at))
        .limit(limit)
    )
    result = await db.execute(query)
    records = result.scalars().all()

    return [
        SensorDataResponse(
            id=str(r.id),
            truck_id=r.truck_id,
            commodity=r.commodity,
            temperature=r.temperature,
            humidity=r.humidity,
            gps_lat=r.gps_lat,
            gps_lon=r.gps_lon,
            battery=r.battery,
            door_status=r.door_status,
            market_price=r.market_price,
            quantity=r.quantity,
            weather_condition=r.weather_condition,
            spoilage_score=r.spoilage_score,
            arbitrage_score=r.arbitrage_score,
            recorded_at=r.recorded_at,
        )
        for r in records
    ]


@router.get("/trucks/locations", response_model=List[TruckLocation])
async def get_truck_locations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current GPS locations of all active trucks."""
    # Get latest reading for each truck with GPS data
    latest_ids = (
        select(
            SensorData.id,
            func.row_number().over(
                partition_by=SensorData.truck_id,
                order_by=desc(SensorData.recorded_at),
            ).label("rn"),
        )
        .where(
            SensorData.user_id == current_user.id,
            SensorData.gps_lat.isnot(None),
            SensorData.gps_lon.isnot(None),
        )
        .subquery()
    )

    query = (
        select(SensorData)
        .where(SensorData.user_id == current_user.id, SensorData.id.in_(
            select(latest_ids.c.id).where(latest_ids.c.rn == 1)
        ))
        .order_by(SensorData.truck_id)
    )
    result = await db.execute(query)
    records = result.scalars().all()

    return [
        TruckLocation(
            truck_id=r.truck_id,
            gps_lat=r.gps_lat,
            gps_lon=r.gps_lon,
            commodity=r.commodity,
            temperature=r.temperature,
            spoilage_score=r.spoilage_score,
            recorded_at=r.recorded_at,
        )
        for r in records
    ]


@router.get("/stats/{truck_id}", response_model=dict)
async def get_truck_stats(
    truck_id: str,
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get statistical summary for a specific truck."""
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    query = select(SensorData).where(
        SensorData.user_id == current_user.id,
        SensorData.truck_id == truck_id,
        SensorData.recorded_at >= start_date,
    )
    result = await db.execute(query)
    records = result.scalars().all()

    if not records:
        return {
            "truck_id": truck_id,
            "readings_count": 0,
            "avg_temperature": 0,
            "avg_humidity": 0,
            "avg_spoilage_score": 0,
            "temperature_range": {"min": 0, "max": 0},
            "humidity_range": {"min": 0, "max": 0},
        }

    temps = [r.temperature for r in records if r.temperature is not None]
    hums = [r.humidity for r in records if r.humidity is not None]
    spoils = [r.spoilage_score for r in records if r.spoilage_score is not None]

    return {
        "truck_id": truck_id,
        "readings_count": len(records),
        "avg_temperature": round(sum(temps) / len(temps), 2) if temps else 0,
        "avg_humidity": round(sum(hums) / len(hums), 2) if hums else 0,
        "avg_spoilage_score": round(sum(spoils) / len(spoils), 2) if spoils else 0,
        "temperature_range": {
            "min": min(temps) if temps else 0,
            "max": max(temps) if temps else 0,
        },
        "humidity_range": {
            "min": min(hums) if hums else 0,
            "max": max(hums) if hums else 0,
        },
    }


def calculate_spoilage_score(temperature: float, humidity: float, commodity: str) -> float:
    """Calculate a spoilage risk score based on temperature and humidity.

    Score ranges from 0 (no risk) to 1 (high risk). The target ranges vary by
    commodity, so different products can have different "ideal" storage bands.
    """

    commodity_name = (commodity or "").strip().lower()
    profiles = {
        "berries": {"temp_low": 2, "temp_high": 8, "humidity_low": 85, "humidity_high": 95},
        "grains": {"temp_low": 10, "temp_high": 15, "humidity_low": 50, "humidity_high": 60},
        "leafy greens": {"temp_low": 0, "temp_high": 4, "humidity_low": 90, "humidity_high": 98},
        "lettuce": {"temp_low": 0, "temp_high": 4, "humidity_low": 90, "humidity_high": 98},
        "meat": {"temp_low": 0, "temp_high": 2, "humidity_low": 90, "humidity_high": 95},
        "dairy": {"temp_low": 2, "temp_high": 4, "humidity_low": 85, "humidity_high": 90},
    }
    profile = profiles.get(commodity_name, {"temp_low": 2, "temp_high": 8, "humidity_low": 85, "humidity_high": 95})

    def _temperature_score(value: float, low: float, high: float) -> float:
        if low <= value <= high:
            return 0.0
        if value < low:
            delta = low - value
            if delta <= 2:
                return 0.2
            if delta <= 5:
                return 0.4
            return 0.8
        delta = value - high
        if delta <= 3:
            return 0.3
        if delta <= 8:
            return 0.6
        return 1.0

    def _humidity_score(value: float, low: float, high: float) -> float:
        if low <= value <= high:
            return 0.0
        if value < low:
            delta = low - value
            if delta <= 10:
                return 0.2
            return 0.5
        delta = value - high
        if delta <= 10:
            return 0.3
        if delta <= 20:
            return 0.6
        return 0.8

    temp_score = _temperature_score(float(temperature), float(profile["temp_low"]), float(profile["temp_high"]))
    humidity_score = _humidity_score(float(humidity), float(profile["humidity_low"]), float(profile["humidity_high"]))

    combined_score = (temp_score * 0.7) + (humidity_score * 0.3)
    return round(min(max(combined_score, 0.0), 1.0), 2)
