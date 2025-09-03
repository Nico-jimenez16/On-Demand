from motor.motor_asyncio import AsyncIOMotorDatabase
from models.service_request import ServiceRequest, ServiceAssignment
from schemas.request import RequestCreate
from bson import ObjectId
from datetime import datetime
from typing import List


async def create_request(db: AsyncIOMotorDatabase, req: RequestCreate, client_id: int):
    request_data = {
        "title": req.title,
        "description": req.description,
        "location": req.location,
        "time_window": req.time_window,
        "client_id": client_id,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    result = await db["service_requests"].insert_one(request_data)
    request_data["_id"] = result.inserted_id
    
    return ServiceRequest(**request_data)


async def list_available_requests(db: AsyncIOMotorDatabase) -> List[ServiceRequest]:
    cursor = db["service_requests"].find({"status": "pending"})
    requests = []
    async for doc in cursor:
        requests.append(ServiceRequest(**doc))
    return requests


async def accept_request(db: AsyncIOMotorDatabase, request_id: str, provider_id: int):
    # Find the request
    request_doc = await db["service_requests"].find_one({"_id": ObjectId(request_id)})
    if not request_doc or request_doc.get("status") != "pending":
        return None

    # Create assignment
    assignment_data = {
        "request_id": request_id,
        "provider_id": provider_id,
        "status": "accepted"
    }
    await db["service_assignments"].insert_one(assignment_data)

    # Update request status
    await db["service_requests"].update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": "assigned"}}
    )

    # Return updated request
    updated_request = await db["service_requests"].find_one({"_id": ObjectId(request_id)})
    return ServiceRequest(**updated_request)
