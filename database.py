#This is the database connection file

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Charvi%40123@127.0.0.1:3108/gym_tracker"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine) #this is the session factory that will create new sessions for us
Base = declarative_base() #this is the base class for our models

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()