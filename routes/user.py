from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import user
from model.user import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "first_project"
ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(user_id: int):
    data = {"user_id": user_id}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

@router.post("/signup")
def signup(name: str, email: str, password: str, weight: float, height: float, db: Session = Depends(get_db)):
    #db: Session = Depends(get_db): This is the most important part.
    #It tells FastAPI: "Before you run this function,
    #  go run get_db to get a fresh database connection,
    #  and call it db so I can use it here."
    hashed_password = pwd_context.hash(password)
    new_user = User(name=name, email=email, password=hashed_password, weight=weight, height=height)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully!"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(password, user.password): #verify(plain password, hashed_password)
        raise HTTPException(status_code=400, detail="Incorrect password")
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/get_user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail= "User not found")
    return {"user_id": user.user_id, "username": user.username, "weight": user.weight, "height": user.height}
