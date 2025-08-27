from http.client import HTTPException
from pydantic import ValidationError
from json_repair import repair_json
from openai import OpenAI
from dotenv import load_dotenv
import uuid
import os
import json

from app.prompts import SYSTEM_PROMPT, USER_PROMPT
from app.schema.defintion import Definition

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

def extract_definitions_and_concepts(input_text: str, doc_id, section_id):
    definitions = llm_extraction(input_text)
    bei_model = map_to_beimodel(definitions, doc_id, section_id)
    return bei_model


def llm_extraction(text: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{USER_PROMPT}\n {text}\n\n"}
        ]
    )
    # Parse JSON output
    try:
        raw = response.choices[0].message.content
        repaired = repair_json(raw)
        concepts = json.loads(repaired)
    except:
        return HTTPException("Failed to extract concepts from response. Invalid JSON")

    results = []
    for item in concepts:
        try:
            results.append(Definition(**item).dict())
        except ValidationError as e:
            return {
                "error": "Schema validation failed",
                "details": e.errors(),
                "raw_item": item
            }

    return results


def map_to_beimodel(parsed_output: list, doc_id="doc5000Definitions", section_id="5000-01") -> dict:
    """
    Maps the simple LLM extraction schema into BEIMODEL JSON structure.
    """
    concepts = []

    for item in parsed_output:
        # generate random id according to wb standard
        concept_id = "n" + uuid.uuid4().hex[:6]

        # map subclass_of and see_also into relations
        relations = []
        for sc in item.get("subclass_of", []):
            relations.append({"to": sc, "type": "subclassOf"})
        for sa in item.get("see_also", []):
            relations.append({"to": sa, "type": "seeAlso"})

        # map alternative terms into labels
        labels = [
            {"type": "AlternativeLabel", "value": alt}
            for alt in item.get("alternative_terms", [])
        ]

        # build BEI concept object
        concept = {
            "_id": concept_id,
            "label": item["concept"],
            "type": "Term",
            "sourceReferences": [
                {
                    "type": "crDescription",
                    "sourceId": doc_id,
                    "sectionId": section_id
                }
            ],
            "textFragments": [
                {"type": "Definition", "value": item["definition"]}
            ],
            "relations": relations,
            "labels": labels
        }

        concepts.append(concept)

    # wrap into BEIMODEL JSON
    return {
        "label": f"Concepts - extracted - TermsAndConcepts for source {doc_id} from section {section_id}",
        "dsl": "TermsAndConcepts",
        "concepts": concepts
    }
