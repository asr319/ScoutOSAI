import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Override the database URL so tests use a local SQLite file
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Import engine after setting DATABASE_URL so it picks up the test URI
from app.db import engine
from app.models.user import Base as UserBase, User
from app.models.memory import Base as MemoryBase, Memory

# Ensure all tables exist for the test database
# Copy the user table onto the memory metadata so SQLAlchemy resolves the
# foreign key correctly during table creation and inserts.
User.__table__.to_metadata(MemoryBase.metadata)
MemoryBase.metadata.create_all(bind=engine)

# No fixtures are required here, but this file ensures the test DB is initialised

