import ollama

from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

def get_cats(info_slide: str, motion: str):
    
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
        categories: set[Category]
        
    categories = [c.value for c in Category]
    categories_str = ",".join(categories)
    prompt =  f"""
You are a debate category classifier.

Task:
Given the info slide and motion, choose all and only the categories from `Possible Categories` that are associated with the text given.

Inputs:
- Info Slide: {info_slide}
- Motion: {motion}
- Possible Categories: {categories_str}

Instructions:
- Only include a category if the association is clear and direct.
- Do NOT include categories that are only tangentially or indirectly related.
- If none of the categories are clearly relevant, return an empty list.

Output format (JSON only, no explanation):
["Category 1", "Category 2", ...]
"""
    
    deepseek_response = ollama.chat(
    model='gemma2:2b',
    messages=[{'role': 'user',
               'content': prompt}],
    format=CategoryList.model_json_schema(),  # Use Pydantic to generate the schema
    options={'temperature': 0},  # Make responses more deterministic
  )
    parsed = CategoryList.model_validate_json(deepseek_response.message.content)
    return [i.value for i in parsed.categories]