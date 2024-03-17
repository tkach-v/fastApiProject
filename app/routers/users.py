from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.db import models
from app.db.connection import get_db
from app.schemas.users import UserGet, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", summary="list of users", response_model=list[UserGet])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get("/{id}", summary="User by id", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", summary="Create a new user", response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.patch("/{id}", response_model=UserGet, summary="Update user by ID")
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{id}", summary="Delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
