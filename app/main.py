from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(title="Task Manager API", version="0.2.0")

# Register the tasks router
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

