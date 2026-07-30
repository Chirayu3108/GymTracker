from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# ----------- Project File Imports --------------------------------
from app.api.deps import get_current_user 
from app.models.user import User
from app.schemas.user import UserRead
# -----------------------------------------------------------------

router = APIRouter(prefix="/users", tags = ["users"])

# ------------------------- User Endpoints ------------------------
@router.get("/me", response_model= UserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
  return current_user
# -----------------------------------------------------------------
