from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat import router as chat_router
from src.api.orders import router as orders_router
from src.api.admin import router as admin_router

try:
    from src.api.voice import router as voice_router
except Exception:
    voice_router = None


app = FastAPI(
    title="SnapServe AI",
    description="Multilingual AI Voice Assistant for Departmental Store",
    version="1.0.0"
)


# CORS - Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Register API Routes

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"]
)


app.include_router(
    orders_router,
    prefix="/api/orders",
    tags=["Orders"]
)


if voice_router:
    app.include_router(
        voice_router,
        prefix="/api/voice",
        tags=["Voice"]
    )


app.include_router(
    admin_router,
    prefix="/api/admin",
    tags=["Admin"]
)



# Application Health Check

@app.get("/")
def home():

    return {
        "app": "SnapServe AI",
        "status": "running",
        "version": "1.0.0"
    }



@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }



# Startup Event

@app.on_event("startup")
async def startup():

    print("🚀 SnapServe AI Started")



# Shutdown Event

@app.on_event("shutdown")
async def shutdown():

    print("🛑 SnapServe AI Stopped")