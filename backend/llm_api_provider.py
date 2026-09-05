from google import genai
import os
import time
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

MODEL_NAME = "gemini-3.7-flash"

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


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.ReadError, httpx.ConnectError, httpx.TimeoutException)),
)
def embed_text(text: str) -> list[float]:
    """
    Turns text into a vector (list of numbers) representing its meaning.
    Single entry point — swap provider here only.

    STEP: @retry decorator add kiya.
    WHY: Network glitch (jaisa WinError 10053) ki wajah se ye call kabhi
    kabhi fail ho jaati hai — isse poora upload crash ho jata tha. Ab
    agar fail ho, ye automatically 3 baar tak dubara try karega, har
    baar thoda zyada wait karke, taaki temporary network issue khud
    resolve ho sake.
    """
    result = _client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values