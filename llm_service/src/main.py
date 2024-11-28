from fastapi import FastAPI
from src.routers.llm_router import llm_router
from src.routers.chatbot import chatbot_router
from src.routers.hr_assistant import hr_assistant_router


def create_app() -> FastAPI:
    app = FastAPI(title='LLM Service')
    app.include_router(chatbot_router)  
    app.include_router(llm_router)
    app.include_router(hr_assistant_router)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True)