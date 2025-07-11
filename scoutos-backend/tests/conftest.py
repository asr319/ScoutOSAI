import os

# Override the database URL so tests use a local SQLite file
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Import engine after setting DATABASE_URL so it picks up the test URI
from app.db import engine
from app.models.base import Base

# Import models so their metadata is registered with Base
from app.models import user as user_model, memory as memory_model

# Create all tables for the test database
Base.metadata.create_all(bind=engine)

# No fixtures are required here, but this file ensures the test DB is initialised

