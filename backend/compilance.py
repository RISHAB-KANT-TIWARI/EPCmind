import json
from exctractors import extract_file
from llm_api_provider import ask_ai

SPEC_PATH = "Sample_docs/UPS_System_Specification.docx"
SUBMITTAL_PATH = "Sample_docs/UPS_Vendor_Submittal_26-33-53-01.pdf"

def run_compliance_check():
    spec = extract_file(SPEC_PATH)
    submittal = extract_file(SUBMITTAL_PATH)

    prompt = f"""SPECIFICATION:
{spec['text']}

VENDOR SUBMITTAL:
{submittal['text']}

Compare every relevant requirement (battery autonomy, capacity, efficiency, topology, warranty, etc.) in the specification against the vendor submittal.

Respond with ONLY a JSON array, no markdown formatting, no explanation, no code fences. Each item must have exactly these fields:
- "requirement": short name of what's being compared
- "specified_value": the value from the specification, or "Not stated" if absent
- "submitted_value": the value from the submittal, or "Not stated" if absent
- "status": exactly one of "Match", "Deviation", or "Cannot verify"
- "severity": "Critical", "Moderate", or "Low" if status is "Deviation", otherwise null

IMPORTANT: If either specified_value or submitted_value is "Not stated", status MUST be "Cannot verify" — never "Match". A match requires both values to be actually present and equivalent.
Example format:
[{{"requirement": "Battery Autonomy", "specified_value": "15 minutes", "submitted_value": "10 minutes", "status": "Deviation", "severity": "Critical"}}]
"""

    raw_response = ask_ai(prompt)

    # Gemini sometimes wraps JSON in ```json fences even when told not to — strip defensively
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    try:
        results = json.loads(cleaned)
    except json.JSONDecodeError:
        # If Gemini didn't return valid JSON, fail loudly instead of crashing the endpoint
        return []

    return results


import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPLIANCE_FILE = os.path.join(BASE_DIR, "last_compliance_check.json")

def save_compliance_results(results):
    data = {
        "results": results,
        "ran_at": datetime.now().isoformat(),
    }
    with open(COMPLIANCE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return data

def load_compliance_results():
    if not os.path.exists(COMPLIANCE_FILE):
        return {"results": [], "ran_at": None}
    with open(COMPLIANCE_FILE, "r") as f:
        return json.load(f)