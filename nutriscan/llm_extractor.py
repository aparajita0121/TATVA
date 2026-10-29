
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def extract_with_llm(ocr_text: str) -> dict:
    """Extract structured nutrition data using the local LLM."""

    if not ocr_text.strip():
        raise ValueError("OCR text is empty.")

    prompt = f"""
You are a food-label OCR data extraction assistant.

Extract only values explicitly supported by the OCR text.

STRICT RULES:
1. Never invent, calculate, multiply, or modify values.
2. Never use an RDA percentage as a nutrient measurement.
3. If the measurement basis is unclear, use "unknown".
4. Missing or unclear nutrient values must be null.
5. Numeric measurements must be JSON numbers, not strings.
6. Units must be kcal, g, mg, ml, or null.
7. Do not assume that values are per 100 g.
8. Return valid JSON only.

Use this exact structure:
{{
  "product_name": null,
  "serving_size": null,
  "energy": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }},
  "protein": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }},
  "carbohydrates": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }},
  "total_sugars": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }},
  "total_fat": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }},
  "saturated_fat": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }},
  "sodium": {{
    "value": null,
    "unit": null,
    "basis": "unknown"
  }}
}}

OCR text:
{ocr_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0}
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()
    raw_response = result.get("response", "")

    if not raw_response:
        raise ValueError("Ollama returned an empty response.")

    data = json.loads(raw_response)

    if not isinstance(data, dict):
        raise ValueError("LLM response must be a JSON object.")

    # Ensure the response follows the new schema.
    required_fields = [
        "product_name",
        "serving_size",
        "energy",
        "protein",
        "carbohydrates",
        "total_sugars",
        "total_fat",
        "saturated_fat",
        "sodium"
    ]

    missing = [field for field in required_fields if field not in data]

    if missing:
        raise ValueError(f"Missing fields in LLM response: {missing}")

    return data
