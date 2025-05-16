from pydantic import BaseModel
from typing import Optional, List

class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None

class SchemaListResponse(BaseModel):
    schemas: List[str]
    message: Optional[str] = None
