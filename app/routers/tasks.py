from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TaskModel
from app.schemas import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Shortcut type: "a DB session injected by FastAPI"
DbSession = Annotated[Session, Depends(get_db)]


def get_task_or_404(db: Session, task_id: int) -> TaskModel:
    """Return the task or raise a 404 error if it does not exist."""
    task = db.get(TaskModel, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("/", response_model=list[Task])
def list_tasks(db: DbSession, completed: bool | None = None):
    """Return all tasks, optionally filtered by completion status."""
    query = select(TaskModel).order_by(TaskModel.id)
    if completed is not None:
        query = query.where(TaskModel.completed == completed)
    return db.scalars(query).all()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: DbSession):
    """Create a new task."""
    task = TaskModel(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)  # reload the object to get the generated id
    return task


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: DbSession):
    """Return a single task by id."""
    return get_task_or_404(db, task_id)


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate, db: DbSession):
    """Partially update a task (only the fields sent by the client)."""
    task = get_task_or_404(db, task_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: DbSession):
    """Delete a task."""
    task = get_task_or_404(db, task_id)
    db.delete(task)
    db.commit()