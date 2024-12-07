from pydantic import BaseModel
from typing import List

class Genres(BaseModel):
    genres: List[str] | None = None