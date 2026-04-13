"""
database.py -- Database connection setup

This file creates two things:
1. Engine: the actual connection to PostgreSQL (like opening a phone line)
2. SessionLocal: a factory that creates "sessions" (individual conversations
   with the database -- you open one, do some work, then close it)

The get_db() function is a "dependency" that FastAPI uses:
  - Before each request: opens a database session
  - After each request: closes it (even if there was an error)
  This prevents connection leaks.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

# Create the engine -- this is the connection pool to PostgreSQL
# pool_pre_ping=True: checks if the connection is alive before using it
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Session factory -- each call to SessionLocal() gives a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that provides a database session per request.

    Usage in a route:
        @app.get("/something")
        def my_route(db: Session = Depends(get_db)):
            # use db here
            ...

    The 'yield' makes this a generator:
    - Everything before yield runs BEFORE the request
    - Everything after yield runs AFTER the request (cleanup)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
