from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    createdOn: datetime

    class Config:
        from_attributes = True
