from sqlalchemy import Column, Integer, String
from database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    