from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from src.api.auth import router as auth_router
from src.api.chat import router as chat_router
from src.api.inventory import router as inventory_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(inventory_router)