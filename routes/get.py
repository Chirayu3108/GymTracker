from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model.user import User
from model.exercise import Exercise
from model.workout import Workout
from model.session import Session as SessionModel
from model.workout_exercise import WorkoutExercise
from services.session_creation import create_workout, create_exercise, add_exercise_to_workout

router = APIRouter()


#SESSION VALUES
@router.get("/all_sessions")
def get_all_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user_id).all()
    return sessions

@router.get("/get_session")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

#WORKOUT VALUES
@router.get("/all_workouts")
def get_all_workouts(user_id: int, db: Session = Depends(get_db)):
    workouts = db.query(Workout).filter(Workout.user_id == user_id).all()
    return workouts

@router.get("/get_workout")
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.workout_id == workout_id).first()
    exercises = db.query(Exercise).join(WorkoutExercise).filter(WorkoutExercise.workout_id == workout_id).all()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return {"workout": workout, "exercises": exercises}

#EXERCISE VALUES
@router.get("/get_exercise")
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise