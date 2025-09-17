# microservice_servicerequest/services/request_service.py
from typing import List
from ..models.service_request import ServiceRequest
from ..schemas.request import RequestCreate
from ..core.config import settings
from ..core.exceptions import RequestNotPendingError, RequestNotFoundException, InvalidIdError
from ..core.repositories.request_repository import ServiceRequestRepository
from datetime import datetime
from ..models.service_request import StatusEnum

class RequestService:
    """
    Clase de servicio para la lógica de negocio de solicitudes de servicio.
    Utiliza el patrón Repository para abstraer el acceso a la base de datos.
    """
    def __init__(self, repository: ServiceRequestRepository):
        self.repository = repository

    async def create_request(self, req: RequestCreate, client_id: int) -> ServiceRequest:
        """Crea una nueva solicitud de servicio con el estado inicial 'pending'."""
        request_data = {
            "title": req.title,
            "description": req.description,
            "location": req.location,
            "time_window": req.time_window,
            "client_id": client_id,
            "status": StatusEnum.PENDING,
            "created_at": datetime.utcnow()
        }
        try:
            return await self.repository.create(request_data)
        except InvalidIdError:
            raise RequestNotFoundException(detail=f"Create_Request with not found.")


    async def list_requests(self) -> List[ServiceRequest]:
        return await self.repository.get_all()

    async def list_available_requests(self) -> List[ServiceRequest]:
        """Obtiene todas las solicitudes de servicio con estado 'pending'."""
        return await self.repository.find_available_requests()

    async def accept_request(self, request_id: str, provider_id: int) -> ServiceRequest:
        """
        Permite a un proveedor aceptar una solicitud de servicio pendiente.
        
        Levanta excepciones si la solicitud no se encuentra o no está pendiente.
        """
        try:
            request = await self.repository.get_by_id(request_id)
            if not request:
                raise RequestNotFoundException()
            
            if request.status != StatusEnum.PENDING:
                raise RequestNotPendingError()

            assignment_data = {
                "request_id": request_id,
                "provider_id": provider_id,
                "status": StatusEnum.ASSIGNED,
                "created_at": datetime.utcnow()
            }
            await self.repository.create_assignment(assignment_data)

            updated_request = await self.repository.update_status(request_id, StatusEnum.ASSIGNED)
            if not updated_request:
                raise RequestNotFoundException()
            
            return updated_request
        except InvalidIdError:
            raise RequestNotFoundException(detail=f"Request with ID {request_id} not found.")