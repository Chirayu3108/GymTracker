from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from model.user import User

router = APIRouter()

@router.post("/signup")
def signup(name: str, email: str, password: str, db: Session = Depends(get_db)):
    #db: Session = Depends(get_db): This is the most important part.
    #It tells FastAPI: "Before you run this function,
    #  go run get_db to get a fresh database connection,
    #  and call it db so I can use it here."
    new_user = User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully!"}


