from pydantic import BaseModel
from typing import Optional

class CompanyProductTaxUpsert(BaseModel):
    id: str
    company_id: str
    product_id: str

    ncm: Optional[str] = None
    cest: Optional[str] = None
    cfop_saida_padrao: Optional[str] = None
    origem_mercadoria: Optional[str] = None

    cst_icms: Optional[str] = None
    csosn: Optional[str] = None

    aliquota_icms: Optional[float] = None
    aliquota_pis: Optional[float] = None
    aliquota_cofins: Optional[float] = None

    observacoes: Optional[str] = None
