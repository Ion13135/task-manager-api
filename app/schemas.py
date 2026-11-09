from datetime import datetime


from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ------------ Task ----------

class TaskCreate(BaseModel):
    """Data the client sends when creating a task."""
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=3)
    # TEMPORARY: in Lesson 5 (login) this will come from the logged-in user
    owner_id: int


class TaskUpdate(BaseModel):
    """Data the client sends when updating a task (all fields optional)."""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None
    priority: int | None = Field(default=None, ge=1, le=3)


class Task(BaseModel):
    """Task as returned by the API."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 1
    created_at: datetime
    owner_id: int


# ---------- Users ----------


class UserCreated(BaseModel):
    """Data the client sends when registering."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    """User as returned by the API. NEVER includes the password or its hash."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime