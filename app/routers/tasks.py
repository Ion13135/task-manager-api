from fastapi import APIRouter, HTTPException, status

from app.schemas import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Temporary in-memory "database" (we will replace it with a real DB in Lesson 3)
tasks_db: dict[int, Task] = {}
next_id = 1


def get_task_or_404(task_id: int) -> Task:
    """Return the task or raise a 404 error if it does not exist."""
    task = tasks_db.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("/", response_model=list[Task])
def list_tasks():
    """Return all tasks."""
    return list(tasks_db.values())


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate):
    """Create a new task."""
    global next_id
    task = Task(id=next_id, **data.model_dump())
    tasks_db[next_id] = task
    next_id += 1
    return task


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Return a single task by id."""
    return get_task_or_404(task_id)


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate):
    """Partially update a task (only the fields sent by the client)."""
    task = get_task_or_404(task_id)
    updated = task.model_copy(update=data.model_dump(exclude_unset=True))
    tasks_db[task_id] = updated
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task."""
    get_task_or_404(task_id)
    del tasks_db[task_id]