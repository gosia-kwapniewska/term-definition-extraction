from pydantic import BaseModel

class Input(BaseModel):
    text: str
    doc_id: str
    section_id: str