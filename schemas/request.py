from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from ..models.service_request  import StatusEnum


# --------------------------
# Clase para manejar ObjectId
# --------------------------
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

# --------------------------
# Modelo para crear solicitudes
# --------------------------
class RequestCreate(BaseModel):
    title: str
    description: str
    location: str
    time_window: str
    status: str = StatusEnum.PENDING

# --------------------------
# Modelo para respuestas
# --------------------------
class RequestOut(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    location: str
    time_window: str
    status: StatusEnum
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    client_id: str  # si tus documentos MongoDB guardan el id del cliente como string

    model_config = {
        "populate_by_name": True, 
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, datetime: lambda dt: dt.isoformat()},
    }
