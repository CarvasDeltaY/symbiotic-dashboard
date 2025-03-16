from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Settings

# Global Base class for all models
Base = declarative_base()

# Create engine
engine = create_engine(Settings().database_url)

# Create session factory
SessionLocal = sessionmaker(bind=engine)