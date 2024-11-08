from uuid import uuid4
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.core.store import lifespan
from src.routers.chat import chat_router
from src.routers.podcast import gateway_router


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(chat_router)
    app.include_router(gateway_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://atlantys.kz", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)