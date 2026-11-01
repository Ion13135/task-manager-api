from fastapi import FastAPI

from app import models # noqa: F401  (import needed so tables are registered
from app.database import Base, engine
from app.routers import tasks


# Create all tables defined in models.py (does nothing if they already exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API", version="0.3.0")

app.include_router(tasks.router)


@app.get("/")
def read_root():
    """Root endpoint - returns a welcome message."""
    return {"message": "Hello, Backend!"}


@app.get("/health")
def health_check():
    """Health check endpoint - used to verify the server is running."""
    return {"status": "ok"}


# --- Paste your homework endpoints (/about and /hello/{name}) below ---

@app.get("/about")
def get_about():
    """Returns information about the app."""
    return {"app": "Task Manager API", "author": "Ion"}

@app.get("/hello/{name}")
def say_hello(name: str):
    """Returns a personalized greeting."""
    return {"message": f"Hello, {name}!"}

