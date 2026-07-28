import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
  __tablename__ = "users"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
  email: Mapped[str] = mapped_column(unique = True, nullable = False, index = True)
  hashed_password: Mapped[str] = mapped_column(nullable = False)
  display_name: Mapped[str | None] = mapped_column(nullable = True)
  is_active: Mapped[bool] = mapped_column(default = True, nullable = False)
  unit_system: Mapped[str] = mapped_column(default = "metric", nullable = False)
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(server_default = func.now(), onupdate = func.now())

