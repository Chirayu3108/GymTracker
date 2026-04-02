from fastapi import FastAPI
from database import engine, Base
from routes.user import router as user_router
from routes.session_creation import router as session_creation_router
from routes.get import router as get_router

#all model imports
from model.user import User
from model.workout import Workout
from model.exercise import Exercise
from model.session import Session
from model.workout_exercise import WorkoutExercise

app = FastAPI()

Base.metadata.create_all(bind= engine)

app.include_router(user_router)
app.include_router(session_creation_router)
app.include_router(get_router)

@app.get("/")
def home_page():
    return {"message": "Welcome to the Gym Tracker API!"}

