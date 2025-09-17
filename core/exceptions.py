# microservice_servicerequest/core/exceptions.py
from fastapi import HTTPException, status

class RequestNotFoundException(HTTPException):
    def __init__(self, detail: str = "Service request not found"):
        """
        Excepción para cuando una solicitud de servicio no se encuentra.
        Devuelve un código de estado 404 Not Found.
        """
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class RequestNotPendingError(HTTPException):
    def __init__(self, detail: str = "Request status is not pending"):
        """
        Excepción para cuando el estado de una solicitud no es "pending"
        al intentar realizar una acción (ej. aceptar).
        Devuelve un código de estado 409 Conflict.
        """
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InvalidIdError(HTTPException):
    def __init__(self, detail: str = "Invalid ID format"):
        """
        Excepción para cuando el ID proporcionado tiene un formato incorrecto
        (ej. no es un ObjectId válido para MongoDB).
        Devuelve un código de estado 400 Bad Request.
        """
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class RepositoryError(HTTPException):
    def __init__(self, detail: str = "An error occurred in the repository layer"):
        """
        Excepción genérica para errores de bajo nivel en el repositorio
        (ej. problemas con la conexión a la base de datos).
        Devuelve un código de estado 500 Internal Server Error.
        """
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)