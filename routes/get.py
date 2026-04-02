from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model.exercise import Exercise
from model.workout import Workout
from services.session_creation import create_workout, create_exercise, add_exercise_to_workout

router = APIRouter()

@router.post("/get_workout")
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.workout_id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout