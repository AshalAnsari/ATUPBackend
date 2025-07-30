from pydantic import BaseModel
from datetime import date

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str