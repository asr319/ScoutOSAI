from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

env_url = os.getenv("DATABASE_URL")
DATABASE_URL = env_url if env_url else "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
