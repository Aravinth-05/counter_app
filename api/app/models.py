"""
models.py -- Database table definitions

This file tells SQLAlchemy what tables exist in the database and what
columns they have. Think of it as a Python description of your database
structure.

SQLAlchemy is an ORM (Object-Relational Mapper):
  - Instead of writing raw SQL like "SELECT * FROM counters"
  - You write Python like Counter.query.all()
  - SQLAlchemy translates Python -> SQL for you
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

# Base class that all our models (tables) inherit from
Base = declarative_base()


class Counter(Base):
    """
    Represents the 'counters' table in PostgreSQL.

    Each row is a named counter with a value.
    For this app, we only have one row: name="main", value=0
    """

    __tablename__ = "counters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, default="main")
    value = Column(Integer, nullable=False, default=0)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
