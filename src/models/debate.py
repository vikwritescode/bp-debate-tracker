from pydantic import BaseModel, Field
from typing import Literal

class DebateCreate(BaseModel):
    date: str
    position: Literal['OG', 'OO', 'CG', 'CO']
    points: int = Field(ge=0, le=3)
    speaks: int = Field(ge=0, le=100)
    motion: str
    infoslide: str