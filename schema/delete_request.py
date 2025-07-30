from pydantic import BaseModel

class DeleteRequest(BaseModel):
    token: str