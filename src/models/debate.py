from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

class DebateCreate(BaseModel):
    date: str
    position: Literal['OG', 'OO', 'CG', 'CO']
    points: int = Field(ge=0, le=3)
    speaks: int = Field(ge=0, le=100)
    motion: str
    infoslide: str

class Category(str, Enum):
    econ = "Economics"
    ir = "International Relations"
    africa = "Africa"
    art = "Art"
    asia = "Asia"
    children = "Children"
    cities = "Cities"
    criminal_justice = "Criminal Justice"
    culture = "Culture"
    feminism = "Feminism"
    latam = "Latin America"
    law = "Law"
    lgbtq = "LGBTQ+"
    media = "Media"
    medical = "Medical"
    middle_east = "Middle East"
    military = "Military"
    minorities = "Minority Communities"
    philosophy = "Philosophy"
    politics = "Politics"
    religion = "Religion"
    romance = "Romance/Sexuality"
    science = "Science/Technology"
    social_justice = "Social Justice"
    sports = "Sports"
        
    
class CategoryList(BaseModel):
    categories: list[Category]