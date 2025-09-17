from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .routers.routes_requests import router as requests_router
from .core.config import settings
from .core.db.database import client  # Importa el cliente de la base de datos

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# Manejadores de excepciones para un control de errores robusto
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

# Middleware CORS para manejar las peticiones de diferentes orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS.split(","),
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS.split(","),
    allow_headers=settings.CORS_ALLOW_HEADERS.split(","),
)

# Eventos de inicio y apagado para la conexión a la base de datos
@app.on_event("startup")
async def startup_db_client():
    """Conecta el cliente de MongoDB al iniciar la aplicación."""
    app.mongodb_client = client

@app.on_event("shutdown")
async def shutdown_db_client():
    """Cierra la conexión de MongoDB al apagar la aplicación."""
    app.mongodb_client.close()

# Inclusión del router principal de solicitudes
app.include_router(
    requests_router, 
    prefix="/v1/requests",
    tags=["Requests"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_gateway.main:app", host="127.0.0.3", port=settings.app_port, reload=True)