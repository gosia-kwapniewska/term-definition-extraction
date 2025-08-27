from typing import List, Optional
from pydantic import BaseModel

class SourceReference(BaseModel):
    type: str
    sourceId: str
    sectionId: str

class TextFragment(BaseModel):
    type: str
    value: str

class Label(BaseModel):
    type: str
    value: str

class Relation(BaseModel):
    to: str
    type: str  # "subclassOf" or "seeAlso"

class BEIConcept(BaseModel):
    _id: str
    label: str
    type: str = "Term"
    sourceReferences: List[SourceReference]
    textFragments: List[TextFragment]
    relations: Optional[List[Relation]] = []
    labels: Optional[List[Label]] = []

class BEIModel(BaseModel):
    label: str
    dsl: str
    concepts: List[BEIConcept]