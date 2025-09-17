# microservice_servicerequest/core/repositories/service_request_repository.py
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from bson.errors import InvalidId
from ...models.service_request import ServiceRequest, ServiceAssignment
from ..exceptions import InvalidIdError, RepositoryError

class ServiceRequestRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.collection = db[collection_name]

    async def get_all(self) -> List[ServiceRequest]:
        try:
            requests = []
            cursor = self.collection.find({})
            async for doc in cursor:
                requests.append(ServiceRequest(**doc))
            return requests
        except Exception as e:
            raise RepositoryError(f"Error listing all requests: {e}")

    async def get_by_id(self, request_id: str) -> Optional[ServiceRequest]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(request_id)})
            if doc:
                return ServiceRequest(**doc)
            return None
        except InvalidId:
            raise InvalidIdError(f"Invalid ID format: {request_id}")
        except Exception as e:
            raise RepositoryError(f"Error getting request by ID: {e}")

    async def create(self, request_data: dict) -> ServiceRequest:
        try:
            result = await self.collection.insert_one(request_data)
            request_data["_id"] = result.inserted_id
            return ServiceRequest(**request_data)
        except Exception as e:
            raise RepositoryError(f"Error creating request: {e}")

    async def update_status(self, request_id: str, new_status: str) -> Optional[ServiceRequest]:
        try:
            await self.collection.update_one(
                {"_id": ObjectId(request_id)},
                {"$set": {"status": new_status}}
            )
            return await self.get_by_id(request_id)
        except InvalidId:
            raise InvalidIdError(f"Invalid ID format: {request_id}")
        except Exception as e:
            raise RepositoryError(f"Error updating request status: {e}")

    async def find_available_requests(self) -> List[ServiceRequest]:
        try:
            requests = []
            cursor = self.collection.find({"status": "pending"})
            async for doc in cursor:
                requests.append(ServiceRequest(**doc))
            return requests
        except Exception as e:
            raise RepositoryError(f"Error finding available requests: {e}")
            
    async def create_assignment(self, assignment_data: dict) -> ServiceAssignment:
        try:
            result = await self.collection.insert_one(assignment_data)
            assignment_data["_id"] = result.inserted_id
            return ServiceAssignment(**assignment_data)
        except Exception as e:
            raise RepositoryError(f"Error creating assignment: {e}")