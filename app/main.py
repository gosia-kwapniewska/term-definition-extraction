from fastapi import FastAPI

from app.schema.input import TextInput
from app.service.llm_extractor import llm_extraction

app = FastAPI(title="Legal Definitions Extractor API")


@app.post("/extract-definitions")
def extract_definitions(input: TextInput):
    return llm_extraction(input.text)

@app.get("/")
def read_root():
    return {"Hello": "World"}

