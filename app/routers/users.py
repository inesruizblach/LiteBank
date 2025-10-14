"""
API routes for user operations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Check if email already exists
    users = crud.get_users(db)
    for u in users:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    """
    Retrieve all users.
    """
    return crud.get_users(db)
