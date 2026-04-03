from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    workout_id = Column(Integer, ForeignKey("workouts.workout_id"), index=True)
    session_start = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)