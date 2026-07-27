import os
import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from loguru import logger

from src.voice.stt import SpeechToText
from src.voice.tts import TextToSpeech
from src.ai.intent_classifier import IntentClassifier
from src.rag.rag_pipeline import ask

router = APIRouter(
    prefix="",
    tags=["Voice"]
)

stt = SpeechToText()
tts = TextToSpeech()


@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...)
):
    try:
        uploads_dir = "data/uploads"
        if os.path.isfile(uploads_dir):
            os.remove(uploads_dir)
        os.makedirs(uploads_dir, exist_ok=True)

        audio_id = str(uuid.uuid4())
        audio_path = os.path.join(uploads_dir, f"{audio_id}.wav")

        with open(audio_path, "wb") as file:
            file.write(await audio.read())

        logger.info(f"Audio received and saved to {audio_path}")

        # 1. Speech to Text
        user_text = stt.transcribe(audio_path)
        logger.info(f"User said: {user_text}")

        # 2. Intent Detection
        intent_result = IntentClassifier.classify(user_text)
        intent = intent_result["intent"]

        # 3. RAG Pipeline Response
        answer = ask(user_text)

        # 4. Text to Speech
        tts_result = tts.generate(text=answer)

        return {
            "status": "success",
            "transcription": user_text,
            "intent": intent,
            "response": answer,
            "tts_file": tts_result.get("audio_file")
        }

    except Exception as error:
        logger.error(f"Voice API Error: {error}")
        return {
            "status": "error",
            "message": str(error)
        }