from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.service_request import ServiceRequest, ServiceAssignment
from ..schemas.request import RequestCreate
from bson import ObjectId
from datetime import datetime
from typing import List
from ..core.config import settings


async def create_request(db: AsyncIOMotorDatabase, req: RequestCreate, client_id: int):
    request_data = {
        "title": req.title,
        "description": req.description,
        "location": req.location,
        "time_window": req.time_window,
        "client_id": client_id,
        "status": settings.STATUS_PENDING,
        "created_at": datetime.utcnow()
    }
    
    result = await db[settings.COLLECTION_NAME].insert_one(request_data)
    request_data["_id"] = result.inserted_id
    
    return ServiceRequest(**request_data)

async def list_requests(db: AsyncIOMotorDatabase) -> List[ServiceRequest]:
    cursor = db[settings.COLLECTION_NAME].find()
    requests = []
    async for doc in cursor:
        try:
            requests.append(ServiceRequest(**doc))
        except Exception as e:
            print("ERROR PARSEANDO DOC:", e)
    return requests

async def list_available_requests(db: AsyncIOMotorDatabase) -> List[ServiceRequest]:
    cursor = db[settings.COLLECTION_NAME].find({"status": "pending"})
    requests = []
    async for doc in cursor:
        print("DOC ENCONTRADO:", doc)  # 👈 debug
        try:
            requests.append(ServiceRequest(**doc))
        except Exception as e:
            print("ERROR PARSEANDO DOC:", e)
    return requests


async def accept_request(db: AsyncIOMotorDatabase, request_id: str, provider_id: int):
    # Find the request
    request_doc = await db[settings.COLLECTION_NAME].find_one({"_id": ObjectId(request_id)})
    if not request_doc or request_doc.get("status") != "pending":
        return None

    # Create assignment
    assignment_data = {
        "request_id": request_id,
        "provider_id": provider_id,
        "status": "accepted"
    }
    await db[settings.COLLECTION_NAME].insert_one(assignment_data)

    # Update request status
    await db[settings.COLLECTION_NAME].update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": "assigned"}}
    )

    # Return updated request
    updated_request = await db[settings.COLLECTION_NAME].find_one({"_id": ObjectId(request_id)})
    return ServiceRequest(**updated_request)
