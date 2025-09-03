from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from schemas.request import RequestCreate, RequestOut
from services import request_service
from core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=RequestOut)
async def create_request(
    req: RequestCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can create requests")
    return await request_service.create_request(db, req, client_id=current_user["id"])


@router.get("/available", response_model=list[RequestOut])
async def get_available_requests(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "provider":
        raise HTTPException(status_code=403, detail="Only providers can view requests")
    return await request_service.list_available_requests(db)


@router.post("/{request_id}/accept", response_model=RequestOut)
async def accept_request(
    request_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "provider":
        raise HTTPException(status_code=403, detail="Only providers can accept requests")
    request = await request_service.accept_request(db, request_id, provider_id=current_user["id"])
    if not request:
        raise HTTPException(status_code=404, detail="Request not found or not available")
    return request
