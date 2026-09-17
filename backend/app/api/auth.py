"""Authentication API routes: register, login, refresh, profile."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)
from app.models.user import User, UserRole
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    TokenRefresh,
    UserUpdate,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a user and return a pair of signed tokens."""
    existing = await db.execute(
        select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Username or email already registered")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=UserRole.VIEWER,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return _token_response(user)


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate a user with username and password."""
    result = await db.execute(select(User).where(User.username == user_data.username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user account")
    return _token_response(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    """Exchange a valid refresh token for a new token pair."""
    payload = decode_token(token_data.refresh_token)
    if payload.get("type") != "refresh" or not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    result = await db.execute(select(User).where(User.username == payload["sub"]))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return _token_response(user)


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return _user_response(current_user)


@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_data.email is not None and user_data.email != current_user.email:
        duplicate = await db.execute(select(User).where(User.email == user_data.email))
        if duplicate.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already registered")
        current_user.email = user_data.email
    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name
    await db.flush()
    await db.refresh(current_user)
    return _user_response(current_user)


def _user_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value if hasattr(user.role, "value") else str(user.role),
        is_active=user.is_active,
        created_at=user.created_at,
    )


def _token_response(user: User) -> TokenResponse:
    subject = user.username
    return TokenResponse(
        access_token=create_access_token({"sub": subject}),
        refresh_token=create_refresh_token({"sub": subject}),
        user=_user_response(user),
    )
