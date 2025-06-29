from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine, SessionLocal


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize DB tables (for dev/convenience, in prod use alembic or similar)
@app.on_event("startup")
def on_startup():
    """
    Creates tables if they do not exist.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"message": "Healthy"}
