from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.routes_requests import router as requests_router
from startup_shutdown import startup_event, shutdown_event
from core.config import settings

app = FastAPI(
    title="Service Requests Microservice",
    version="1.0.0"
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