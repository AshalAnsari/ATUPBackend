from pydantic import BaseModel
from datetime import datetime

class ActivityRequest(BaseModel):
    token: str
    action: str

class UserActivity(BaseModel):
    token: str

class ActivityResponse(BaseModel):
    action: str
    timestamp: datetime