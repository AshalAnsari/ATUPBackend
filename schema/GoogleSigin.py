from pydantic import BaseModel

class GoogleSigninSchema(BaseModel):
    token: str
    username: str
    email: str
    image: str

class LoggingGoogleSigninSchema(BaseModel):
    token: str