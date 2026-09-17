"""Alerts API routes: list, update, resolve."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    severity: Optional[str] = None,
    alert_type: Optional[str] = None,
    is_resolved: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List alerts with optional filtering."""
    query = select(Alert).where(Alert.user_id == current_user.id)

    if severity:
        query = query.where(Alert.severity == severity)
    if alert_type:
        query = query.where(Alert.alert_type == alert_type)
    if is_resolved is not None:
        query = query.where(Alert.is_resolved == is_resolved)

    query = query.order_by(desc(Alert.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    alerts = result.scalars().all()

    return [
        AlertResponse(
            id=str(a.id),
            truck_id=a.truck_id,
            alert_type=a.alert_type.value if hasattr(a.alert_type, 'value') else a.alert_type,
            severity=a.severity.value if hasattr(a.severity, 'value') else a.severity,
            title=a.title,
            message=a.message,
            value=a.value,
            threshold=a.threshold,
            is_read=a.is_read,
            is_resolved=a.is_resolved,
            created_at=a.created_at,
        )
        for a in alerts
    ]


@router.get("/unread-count", response_model=dict)
async def get_unread_alert_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the count of unread alerts."""
    from sqlalchemy import func

    result = await db.execute(
        select(func.count(Alert.id)).where(
            Alert.user_id == current_user.id, Alert.is_read == False
        )  # noqa: E712
    )
    count = result.scalar() or 0

    return {"unread_count": count}


@router.put("/mark-all-read", response_model=dict)
async def mark_all_alerts_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark all alerts for the current user as read."""
    from sqlalchemy import update as sa_update

    await db.execute(
        sa_update(Alert)
        .where(Alert.user_id == current_user.id, Alert.is_read == False)  # noqa: E712
        .values(is_read=True)
    )
    await db.flush()
    return {"message": "All alerts marked as read"}


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: str,
    update_data: AlertUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an alert (mark as read/resolved)."""
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id, Alert.user_id == current_user.id)
    )
    alert = result.scalar_one_or_none()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    if update_data.is_read is not None:
        alert.is_read = update_data.is_read
    if update_data.is_resolved is not None:
        alert.is_resolved = update_data.is_resolved
        if update_data.is_resolved:
            from datetime import datetime, timezone
            alert.resolved_at = datetime.now(timezone.utc)

    await db.flush()
    await db.refresh(alert)

    return AlertResponse(
        id=str(alert.id),
        truck_id=alert.truck_id,
        alert_type=alert.alert_type.value if hasattr(alert.alert_type, 'value') else alert.alert_type,
        severity=alert.severity.value if hasattr(alert.severity, 'value') else alert.severity,
        title=alert.title,
        message=alert.message,
        value=alert.value,
        threshold=alert.threshold,
        is_read=alert.is_read,
        is_resolved=alert.is_resolved,
        created_at=alert.created_at,
    )
