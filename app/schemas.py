from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Data the client sends when creating a task."""
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class TaskUpdate(BaseModel):
    """Data the client sends when updating a task (all fields optional)."""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class Task(BaseModel):
    """Task as returned by the API."""
    id: int
    title: str
    description: str | None = None
    completed: bool = False