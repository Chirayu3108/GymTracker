import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserRead(BaseModel):
  model_config = ConfigDict(from_attributes = True)

  id: uuid.UUID
  email: EmailStr
  display_name: str | None
  created_at: datetime