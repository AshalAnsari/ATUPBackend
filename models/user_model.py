from sqlalchemy import Column, String, DateTime, Boolean, text, func
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed passwords here
    image = Column(String(255), nullable=True)
    verified = Column(Boolean, nullable=False, server_default=text("false"))
    createdOn = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
