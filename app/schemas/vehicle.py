from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    id: str
    montadora: str
    modelo: str
    ano: int
    motor: Optional[str] = None
    versao: Optional[str] = None
    texto_busca: Optional[str] = None

class VehicleOut(VehicleCreate):
    pass
