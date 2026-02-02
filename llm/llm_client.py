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
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def call_llm(system_prompt: str, user_prompt: str) -> dict:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt
    )

    response = model.generate_content(
        user_prompt,
        generation_config={
            "temperature": 0,
            "response_mime_type": "application/json"
        }
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
