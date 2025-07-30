from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('SQLHOST')}/{os.getenv('DATABASE')}"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL queries

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get DB session in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
