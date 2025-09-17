from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from ..config import settings

# Conexión asíncrona a la base de datos de MongoDB
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.DATABASE_NAME]

def get_service_requests_collection() -> Collection:
    """
    Retorna la colección 'ServiceRequest'. Esta función se usa como una dependencia
    en FastAPI para inyectar la colección directamente en los repositorios.
    """
    return database.get_collection("ServiceRequest")