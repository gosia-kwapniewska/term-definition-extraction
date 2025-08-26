from app.prompts import SYSTEM_PROMPT, USER_PROMPT
import uuid
import openai


def llm_extraction(input_text: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or your chosen model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{USER_PROMPT}\n {input_text}\n\n"}
        ]
    )

    # Parse JSON output
    try:
        concepts = json.loads(response["choices"][0]["message"]["content"])
    except:
        concepts = []

    return {"document_id": str(uuid.uuid4()), "extracted_definitions": concepts}