import json
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini once
client = genai.Client(api_key=GEMINI_API_KEY)


import json
import re
from dotenv import load_dotenv
import os

from llm.prompt import SYSTEM_PROMPT

load_dotenv()

def call_llm(user_prompt: str) -> dict:
    response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser input:\n{user_prompt}"
        )
    
    raw_text = response.text.strip()

    # 🔐 HARDENING: extract JSON if Gemini adds noise
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

    return {
        "intent": "ERROR",
        "error": "Invalid JSON returned by LLM"
    }
