from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
class SessionExercise(Base):
    __tablename__ = "session_exercises"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"))

    sets = Column(Integer)
    reps = Column(Integer)