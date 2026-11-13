from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TaskModel, UserModel
from app.schemas import Task, UserCreated, UserRead
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


DbSession = Annotated[Session, Depends(get_db)]


def get_user_or_404(db: Session, user_id: int) -> UserModel:
    """Return the user or raise a 404 error if it does not exist."""
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=list[UserRead])
def list_users(db: DbSession, skip: int = 0, limit: int = 10):
    """Return all users with pagination."""
    query = select(UserModel).order_by(UserModel.id).offset(skip).limit(limit)
    return db.scalars(query).all()



@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreated, db: DbSession):
    """Register a new user (the password is stored hashed)."""

    # Normalize email to lowercase
    normalized_email = data.email.lower()

    existing = db.scalar(select(UserModel).where(UserModel.email == normalized_email))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )


    user = UserModel(email=normalized_email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: DbSession):
    """Return a single user by id."""
    return get_user_or_404(db, user_id)



@router.get("/{user_id}/tasks", response_model=list[Task])
def list_user_tasks(user_id: int, db: DbSession):
    """Return all tasks that belong to a user."""
    get_user_or_404(db, user_id)
    query = select(TaskModel).where(TaskModel.owner_id == user_id).order_by(TaskModel.id)
    return db.scalars(query).all()



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DbSession):
    """Delete a user and all their tasks (cascade)."""
    user = get_user_or_404(db, user_id)
    db.delete(user)
    db.commit()