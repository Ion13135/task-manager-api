from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Data the client sends when creating a task."""
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=3)


class TaskUpdate(BaseModel):
    """Data the client sends when updating a task (all fields optional)."""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None
    priority: int | None = Field(default=None, ge=1, le=3)


class Task(BaseModel):
    """Task as returned by the API."""
    # from_attributes lets Pydantic read data from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 1