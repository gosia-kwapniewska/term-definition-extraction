from fastapi import FastAPI

from app.schema.input import Input
from app.service.llm_extractor import extract_definitions_and_concepts

app = FastAPI(title="Legal Definitions Extractor API")


@app.post("/extract-definitions")
def extract_definitions(input: Input):
    return extract_definitions_and_concepts(input.text, input.doc_id, input.section_id)

@app.get("/")
def read_root():
    return {"Hello": "World"}

