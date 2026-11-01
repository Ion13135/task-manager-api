from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite database stored in a file named tasks.db in the project root
DATABASE_URL = "sqlite:///./tasks.db"

# The engine manages the actual connection to the database.
# check_same_thread=False is needed for SQLite when used with FastAPI.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# A factory that creates new database sessions
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class for all database models."""


def get_db():
    """Dependency: provide a DB session per request and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()