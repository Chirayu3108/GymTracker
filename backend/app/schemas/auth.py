import uuid
from pydantic import BaseModel, EmailStr, ConfigDict


class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str = "bearer"
