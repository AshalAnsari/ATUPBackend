from pydantic import BaseModel


class ResetSchema(BaseModel):
    email: str

class OTPSchema(BaseModel):
    otp: str