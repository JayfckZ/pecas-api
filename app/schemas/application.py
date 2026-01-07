from pydantic import BaseModel
from typing import Optional

class ApplicationCreate(BaseModel):
    id: str
    product_id: str
    vehicle_id: str
    observacoes: Optional[str] = None

class ApplicationOut(ApplicationCreate):
    pass
