from pydantic import BaseModel, Field
from typing import Literal

class SlugRef(BaseModel):
    name: str
    slug: str

class SpeakerRef(BaseModel):
    name: str
    team: str
    url: str

class TournamentImportModel(BaseModel):
    url: str
    slug: str
    speaker: str
    date: str