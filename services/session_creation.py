'''
This module contains all the functions to create a session
including creating a workout, an exercise and adding an exercise to a workout
'''

from model.session_exercise import SessionExercise
from model.workout import Workout
from model.exercise import Exercise
from model.workout_exercise import WorkoutExercise
from model.session import Session as SessionModel
from sqlalchemy.orm import Session
from datetime import datetime


def create_workout(user_id: int, name: str, db: Session):
    workout = Workout(user_id=user_id, name=name)
    db.add(workout)
    db.commit()
    db.refresh(workout)  # loads the new id back into the object
    return workout


def create_exercise(name: str, db: Session):
    exercise = Exercise(name=name)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def add_exercise_to_workout(workout_id: int, exercise_id: int, db: Session):
    link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id)
    db.add(link)
    db.commit()
    return link 


#session creation functions

def start_session(user_id: int, workout_id: int, db: Session):
    session = SessionModel(user_id=user_id, workout_id=workout_id, session_start= datetime.now())
    workout = db.query(Workout).filter(Workout.workout_id == workout_id).first()
    if not workout:
        raise ValueError('Workout not found')
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def finish_session(session_id: int, db: Session):
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise ValueError('Session not found')
    session.end_time = datetime.now()
    db.commit()
    return {"message": "Session finished successfully", "session_time": session.end_time - session.session_start}

##<!-- Log exercise function -->    
def log_exercise(session_id: int, exercise_id: int, reps: int, sets: int , db: Session):
    # checking for session existence
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise ValueError('Session not found')
    
    log = SessionExercise(session_id=session_id, exercise_id=exercise_id, reps=reps, sets=sets)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log