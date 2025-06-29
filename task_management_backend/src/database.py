"""
Database integration layer using SQLAlchemy for PostgreSQL.
Handles the engine and session setup and defines ORM models for users and tasks.
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()


# PUBLIC_INTERFACE
Base = declarative_base()


# PUBLIC_INTERFACE
def get_database_url():
    """
    Returns the database URL.
    Prioritizes environment variable 'POSTGRES_URL', falls back to local settings.
    """
    return os.getenv('POSTGRES_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')


# PUBLIC_INTERFACE
engine = create_engine(get_database_url(), echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------- SCHEMA DEFINITIONS ----------------


# PUBLIC_INTERFACE
class User(Base):
    """
    SQLAlchemy model for users.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="owner")


# PUBLIC_INTERFACE
class Task(Base):
    """
    SQLAlchemy model for tasks.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    category = Column(String, default="uncategorized")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
