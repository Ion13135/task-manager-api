from fastapi import FastAPI

# Create the application instance
app = FastAPI(title="Task Manager API", version="0.1.0")

@app.get("/")
def read_root():
    """Root endpoint - returns a welcome message."""
    return {"message": "Hello, Backend!"}

@app.get("/healt")
def health_check():
    """Health check endpoint - used to verify the server is running."""
    return {"status": "ok"}

@app.get("/about")
def about():
    """About endpoint - returns app and author info"""
    return {"app": "Task Manager API", "author": "Ion"}

@app.get("/hello/{name}")
def say_hello(name: str):
    """Hello endpoint - greets by name."""
    return {"message": f"Hello, {name}!"}