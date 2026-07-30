from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token


from app.db.sessions import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import UserLogin, Token

router = APIRouter(prefix="/auth", tags = ["auth"])

@router.post("/register", response_model=UserRead)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email = payload.email, hashed_password = hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model= Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return Token(
        access_token= create_access_token(str(user.id)),
        refresh_token= create_refresh_token(str(user.id))
        )

    
    
