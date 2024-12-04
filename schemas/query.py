from pydantic import BaseModel

class SearchRequest(BaseModel):
    name: str | None = None
    genre: str | None = None

