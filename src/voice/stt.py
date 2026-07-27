import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class SpeechToText:


    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )



    def transcribe(
        self,
        audio_file
    ):

        """
        Convert customer voice into text
        """

        with open(
            audio_file,
            "rb"
        ) as file:


            response = self.client.audio.transcriptions.create(

                model="whisper-large-v3",

                file=file

            )


        return response.text