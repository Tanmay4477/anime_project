from sqlmodel import SQLModel, Field, String, ARRAY, Column
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    genres: List[str] = Field(default=None, sa_column=Column(ARRAY(String())))

