from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenLogin(BaseModel):
    token: str