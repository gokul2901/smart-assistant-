# src/core/llm.py

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

LLM_MODELS = [
    {
        "name": "mistral",
        "model": "mistral/mistral-small-latest",
        "keys": ["MISTRAL_API_KEY", "MIST_API_KEY"]
    },
    {
        "name": "glm",
        "model": "glm/glm-4",
        "keys": ["GLM_API_KEY", "GLM_API_KEYS"]
    },
    {
        "name": "grok",
        "model": "xai/grok-beta",
        "keys": ["GROK_API_KEY"]
    }
]


def call_llm(messages):
    for llm in LLM_MODELS:
        api_key = None
        for k in llm["keys"]:
            val = os.getenv(k)
            if val:
                api_key = val
                break

        if not api_key:
            continue

        try:
            response = completion(
                model=llm["model"],
                messages=messages,
                api_key=api_key
            )
            if response and hasattr(response, "choices") and response.choices:
                content = response.choices[0].message.content
                if content:
                    return content
        except Exception:
            continue

    return "I am SnapServe AI assistant for your departmental store. How can I help you today?"


generate_response = call_llm