from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.workout_id"))
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"))