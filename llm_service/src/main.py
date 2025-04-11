from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from src.routers.chatbot import chatbot_router
from src.routers.hr_assistant import hr_assistant_router
from src.routers.llm_router import llm_router
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Swagger",
        version="3.0.3",
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def register_static_docs_routers(app: FastAPI):
    @app.get("/api/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/api/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.55/bundles/redoc.standalone.js",
        )

    @app.get("/api/openapi.json", include_in_schema=False)
    async def get_openapi_json():
        schema = app.openapi()
        print(f"OpenAPI schema requested. Schema size: {len(str(schema))} characters")
        return JSONResponse(content=schema)


def create_app(create_custom_static_urls) -> FastAPI:
    app = FastAPI(
        title="LLM Service",
        docs_url=None if create_custom_static_urls else '/api/docs',
        redoc_url=None if create_custom_static_urls else '/api/redoc',
        openapi_url="/api/openapi.json"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(chatbot_router)
    app.include_router(llm_router)
    app.include_router(hr_assistant_router)
    if create_custom_static_urls:
        register_static_docs_routers(app)
    else:
        @app.get("/api/openapi.json", include_in_schema=False)
        async def get_openapi_json():
            schema = app.openapi()
            return JSONResponse(content=schema)
    app.openapi = custom_openapi
    return app


app = create_app(create_custom_static_urls=True)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True)
