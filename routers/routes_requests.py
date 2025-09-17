from fastapi import APIRouter, Depends, HTTPException
from ..schemas.request import RequestCreate, RequestOut
from ..services.request_service import RequestService
from ..core.security import get_current_user
from ..core.db.database import get_service_requests_collection
from ..core.repositories.request_repository import ServiceRequestRepository
from ..core.config import settings

router = APIRouter()

def get_service_requests_repository(
    collection=Depends(get_service_requests_collection)
) -> ServiceRequestRepository:
    """Proporciona una instancia del repositorio de solicitudes de servicio."""
    return ServiceRequestRepository(db=collection.database, collection_name=settings.COLLECTION_NAME)

def get_request_service(
    repository: ServiceRequestRepository = Depends(get_service_requests_repository)
) -> RequestService:
    """Proporciona una instancia del servicio de solicitudes de servicio."""
    return RequestService(repository)

@router.get("/", response_model=list[RequestOut])
async def list_requests(
    service: RequestService = Depends(get_request_service),
):
    """
    Obtiene todas las solicitudes de servicio.
    """
    return await service.list_requests()

@router.post("/", response_model=RequestOut)
async def create_request(
    req: RequestCreate,
    current_user: dict = Depends(get_current_user),
    service: RequestService = Depends(get_request_service)
):
    """
    Crea una nueva solicitud de servicio.
    Solo clientes pueden crear solicitudes.
    """
    if current_user["type"] != "cliente":
        raise HTTPException(status_code=403, detail="Only clients can create requests")
    
    return await service.create_request(req, client_id=current_user["id"])

@router.get("/available", response_model=list[RequestOut])
async def get_available_requests(
    current_user: dict = Depends(get_current_user),
    service: RequestService = Depends(get_request_service)
):
    """
    Obtiene todas las solicitudes de servicio disponibles.
    Solo proveedores pueden ver solicitudes disponibles.
    """
    if current_user["role"] != "provider":
        raise HTTPException(status_code=403, detail="Only providers can view requests")
    
    return await service.list_available_requests()

@router.post("/{request_id}/accept", response_model=RequestOut)
async def accept_request(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    service: RequestService = Depends(get_request_service)
):
    """
    Permite a un proveedor aceptar una solicitud de servicio pendiente.
    Solo proveedores pueden aceptar solicitudes.
    """
    if current_user["role"] != "provider":
        raise HTTPException(status_code=403, detail="Only providers can accept requests")
    
    return await service.accept_request(request_id, provider_id=current_user["id"])