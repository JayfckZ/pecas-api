from pydantic import BaseModel
from typing import Optional, List

class ProductCreate(BaseModel):
    id: str
    codigo_interno: str
    descricao_principal: str
    marca: Optional[str] = None
    unidade: Optional[str] = None
    ean: Optional[str] = None
    codigo_fabricante: Optional[str] = None
    imagem_url: Optional[str] = None
    category_id: Optional[str] = None
    subcategory_id: Optional[str] = None
    ativo: bool = True

    aliases: List[str] = []
    similar_product_ids: List[str] = []


class ProductOut(BaseModel):
    id: str
    codigo_interno: str
    descricao_principal: str
    marca: Optional[str]
    unidade: Optional[str]
    ean: Optional[str]
    codigo_fabricante: Optional[str]
    imagem_url: Optional[str]
    category_id: Optional[str]
    subcategory_id: Optional[str]
    ativo: bool

    aliases: List[str]
    similar_product_ids: List[str]
