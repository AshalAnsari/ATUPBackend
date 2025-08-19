from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean
import uuid
from datetime import datetime, timezone, timedelta

Base = declarative_base()

class ResetModel(Base):
    __tablename__ = 'reset'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False)  
    otp_hash = Column(String(128), nullable=False) 
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(minutes=10), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
