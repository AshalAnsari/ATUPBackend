from pydantic import BaseModel
from typing import Optional

class EditRequest(BaseModel):
    image: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
