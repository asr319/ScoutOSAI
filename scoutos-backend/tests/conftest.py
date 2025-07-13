import os
import sys
from cryptography.fernet import Fernet

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from cryptography.fernet import Fernet

# Override the database URL so tests use a local SQLite file
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["APP_ENCRYPTION_KEY"] = Fernet.generate_key().decode()

# Import engine after setting DATABASE_URL so it picks up the test URI
from app.db import engine  # noqa: E402
from app.models.base import Base  # noqa: E402

# Import models so their metadata is registered with Base
from app.models import user as user_model  # noqa: F401,E402
from app.models import memory as memory_model  # noqa: F401,E402

# Create all tables for the test database
Base.metadata.create_all(bind=engine)

# No fixtures are required; this file initializes the test DB
