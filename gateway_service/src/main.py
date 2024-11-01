from fastapi import FastAPI
from routers.podcast import gateway_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(gateway_router)
    return app

app = create_app()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)