# src/call_agent/stt_handler.py


import os
from openai import AsyncOpenAI


client = AsyncOpenAI(

    api_key=os.getenv(
        "GROQ_API_KEY"
    ),

    base_url=
    "https://api.groq.com/openai/v1"

)



class STTHandler:


    async def transcribe(
        self,
        audio_file
    ):


        result = await client.audio.transcriptions.create(

            model="whisper-large-v3",

            file=audio_file

        )


        return result.text