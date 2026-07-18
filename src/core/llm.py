# src/core/llm.py

from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

def generate_response(messages):

    models = [
        ("gemini/gemini-2.5-flash", os.getenv("GEMINI_API_KEY")),
        ("grok/grok-4", os.getenv("GROK_API_KEY")),
        ("mistral/mistral-large-latest", os.getenv("MIST_API_KEY"))
    ]

    for model, key in models:
        try:
            response = completion(
                model=model,
                api_key=key,
                messages=messages
            )

            return response.choices[0].message.content

        except Exception:
            continue

    return "Unable to generate response"