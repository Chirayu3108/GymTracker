from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model.exercise import Exercise
from model.workout import Workout
from services.session_creation import create_workout, create_exercise, add_exercise_to_workout

router = APIRouter()

@router.post("/create_workout")
def create_workout_route(user_id: int, workout_name: str, db: Session = Depends(get_db)):
    workout = create_workout(user_id=user_id, name=workout_name, db=db)
    return workout

@router.post("/create_exercise")
def create_exercise_route(exercise_name: str, db: Session = Depends(get_db)):
    exercise = create_exercise(name=exercise_name, db=db)
    return exercise
    
@router.post("/add_exercise_to_workout")
def add_exercise_to_workout_route(workout_id: int, exercise_id: int, db: Session = Depends(get_db)):
    link = add_exercise_to_workout(workout_id=workout_id, exercise_id=exercise_id, db=db)
    return link