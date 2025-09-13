from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from ..config import settings

# MongoDB configuration
MONGODB_URL = settings.MONGODB_URL
DATABASE_NAME = settings.DATABASE_NAME

# Async client for FastAPI
client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Sync client for non-async operations if needed
sync_client = MongoClient(MONGODB_URL)
sync_database = sync_client[DATABASE_NAME]

# Collections
service_requests_collection = database["ServiceRequest"]
service_assignments_collection = database["service_assignments"]

def get_database():
    """Get async MongoDB database instance"""
    return database

def get_sync_database():
    """Get sync MongoDB database instance"""
    return sync_database