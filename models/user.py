from sqlmodel import SQLModel, Field
from typing import List, Optional



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    genres: None | str = None

