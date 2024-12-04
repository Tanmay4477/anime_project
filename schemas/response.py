from pydantic import BaseModel

class ResponseWraper(BaseModel):
    status: int
    message: str
    data: None | str | int
