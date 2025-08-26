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


def llm_extraction(input_text: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{USER_PROMPT}\n {input_text}\n\n"}
        ]
    )

    # Parse JSON output
    try:
        raw = response["choices"][0]["message"]["content"]
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

    return {"document_id": str(uuid.uuid4()), "extracted_definitions": results}