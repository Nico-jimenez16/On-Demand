from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.routes_requests import router as requests_router
from .core.db.startup_shutdown import startup_event, shutdown_event
from .core.config import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# CORS middleware usando settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS.split(","),
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS.split(","),
    allow_headers=settings.CORS_ALLOW_HEADERS.split(","),
)

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

app.include_router(
    requests_router, 
    prefix="/v1/requests",
    tags=["Requests"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_gateway.main:app", host="127.0.0.3", port=settings.app_port, reload=True)
