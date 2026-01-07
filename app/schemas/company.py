from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    id: str
    nome: str
    cnpj: Optional[str] = None
    ativo: bool = True

class CompanyOut(CompanyCreate):
    pass
