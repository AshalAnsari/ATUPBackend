from sqlalchemy import Column, String, func, DateTime
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class ActivityModel(Base):
    __tablename__ = "activity"

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50))
    action = Column(String(100))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
