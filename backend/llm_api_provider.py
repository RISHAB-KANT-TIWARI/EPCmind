from google import genai
import os
from dotenv import load_dotenv
# Central config — change provider/model here only

MODEL_NAME = "gemini-2.5-flash"  # or gemini-2.5-pro for higher quality

load_dotenv()
API_KEY = os.getenv("API_KEY")


_client = genai.Client(api_key=API_KEY)

def ask_ai(prompt: str) -> str:
    """
    Single entry point for all AI calls in the project.
    Swap the provider here later without touching any other file.
    """
    response = _client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text