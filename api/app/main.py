"""
main.py -- The FastAPI application

This is the heart of the backend. It defines:
- The API endpoints (URLs your app responds to)
- What happens when each endpoint is hit

FastAPI automatically:
- Validates request data
- Generates interactive docs at /docs (Swagger UI)
- Returns JSON responses
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db, engine
from .models import Base, Counter

# Create all tables in the database (if they don't exist)
# In production you'd use migrations (Alembic), but this is fine for learning
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(
    title="Counter API",
    description="A simple counter microservice for learning Docker, K8s, and monitoring",
    version="1.0.0",
)


def _get_counter(db: Session) -> Counter:
    """
    Helper: get the 'main' counter from the database.
    If it doesn't exist yet, create it with value=0.
    """
    counter = db.query(Counter).filter(Counter.name == "main").first()
    if not counter:
        counter = Counter(name="main", value=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)
    return counter


# ---------- ENDPOINTS ----------


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns 200 OK if the app is running. Doesn't touch the database.
    Used by Docker and Kubernetes to know if the app is alive.
    """
    return {"status": "healthy"}


@app.get("/counter")
def get_counter(db: Session = Depends(get_db)):
    """
    GET /counter -- Read the current count.

    How it works:
    1. FastAPI sees Depends(get_db) and opens a DB session
    2. We query the counters table for the row named "main"
    3. Return the value as JSON
    4. FastAPI closes the DB session (via get_db's finally block)
    """
    counter = _get_counter(db)
    return {"name": counter.name, "value": counter.value}


@app.post("/counter/increment")
def increment_counter(db: Session = Depends(get_db)):
    """
    POST /counter/increment -- Add 1 to the counter.

    POST (not GET) because we're CHANGING data, not just reading it.
    This is a REST convention:
      GET = read
      POST = create/modify
    """
    counter = _get_counter(db)
    counter.value += 1
    db.commit()
    db.refresh(counter)
    return {"name": counter.name, "value": counter.value}


@app.post("/counter/decrement")
def decrement_counter(db: Session = Depends(get_db)):
    """POST /counter/decrement -- Subtract 1 from the counter."""
    counter = _get_counter(db)
    counter.value -= 1
    db.commit()
    db.refresh(counter)
    return {"name": counter.name, "value": counter.value}


@app.post("/counter/reset")
def reset_counter(db: Session = Depends(get_db)):
    """POST /counter/reset -- Set the counter back to 0."""
    counter = _get_counter(db)
    counter.value = 0
    db.commit()
    db.refresh(counter)
    return {"name": counter.name, "value": counter.value}
