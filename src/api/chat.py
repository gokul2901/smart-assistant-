from fastapi import APIRouter
from src.rag.rag_pipeline import ask

router = APIRouter()

@router.post("/chat")
def chat(query: str):

    answer = ask(query)

    return {"response": answer}