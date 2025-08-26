from pydantic import BaseModel
from typing import Literal, List

class Definition(BaseModel):
    concept: str
    defined_by: Literal["text", "external reference"]
    definition: str
    alternative_terms: List[str] = []
    subclass_of: List[str] = []
    see_also: List[str] = []