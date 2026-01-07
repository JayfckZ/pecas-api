from pydantic import BaseModel
from typing import Optional

class CompanyProductCreate(BaseModel):
    id: str
    company_id: str
    product_id: str
    ativo: bool = True
    preco_venda: float = 0.0
    preco_custo: float = 0.0
    estoque_atual: int = 0
    estoque_minimo: int = 0
    localizacao: Optional[str] = None

class CompanyProductOut(CompanyProductCreate):
    pass

class InventoryMovementCreate(BaseModel):
    id: str
    company_id: str
    product_id: str
    company_product_id: str
    tipo: str  # IN | OUT | AJUSTE
    quantidade: int
    custo_unitario: Optional[float] = None
    origem: Optional[str] = None
    observacoes: Optional[str] = None
