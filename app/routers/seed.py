from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import (
    Product, ProductAlias, ProductSimilar,
    Vehicle, Application,
    Company, CompanyProduct,
    CompanyProductTax
)

router = APIRouter(prefix="/seed", tags=["Seed"])

# ---------
# Schemas
# ---------
class SeedProduct(BaseModel):
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

class SeedVehicle(BaseModel):
    id: str
    montadora: str
    modelo: str
    ano: int
    motor: Optional[str] = None
    versao: Optional[str] = None
    texto_busca: Optional[str] = None

class SeedApplication(BaseModel):
    id: str
    product_id: str
    vehicle_id: str
    observacoes: Optional[str] = None

class SeedCompany(BaseModel):
    id: str
    nome: str
    cnpj: Optional[str] = None
    ativo: bool = True

class SeedCompanyProduct(BaseModel):
    id: str
    company_id: str
    product_id: str
    ativo: bool = True
    preco_venda: float = 0.0
    preco_custo: float = 0.0
    estoque_atual: int = 0
    estoque_minimo: int = 0
    localizacao: Optional[str] = None

class SeedTax(BaseModel):
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

class SeedPayload(BaseModel):
    products: List[SeedProduct] = []
    vehicles: List[SeedVehicle] = []
    applications: List[SeedApplication] = []
    company: Optional[SeedCompany] = None
    company_products: List[SeedCompanyProduct] = []
    taxes: List[SeedTax] = []

# ---------
# Helpers
# ---------
def upsert_product(db: Session, item: SeedProduct):
    p = db.query(Product).filter(Product.id == item.id).first()
    if not p:
        p = Product(
            id=item.id,
            codigo_interno=item.codigo_interno,
            descricao_principal=item.descricao_principal,
            marca=item.marca,
            unidade=item.unidade,
            ean=item.ean,
            codigo_fabricante=item.codigo_fabricante,
            imagem_url=item.imagem_url,
            category_id=item.category_id,
            subcategory_id=item.subcategory_id,
            ativo=item.ativo,
        )
        db.add(p)
        db.flush()
    else:
        p.codigo_interno = item.codigo_interno
        p.descricao_principal = item.descricao_principal
        p.marca = item.marca
        p.unidade = item.unidade
        p.ean = item.ean
        p.codigo_fabricante = item.codigo_fabricante
        p.imagem_url = item.imagem_url
        p.category_id = item.category_id
        p.subcategory_id = item.subcategory_id
        p.ativo = item.ativo

    # substitui aliases
    db.query(ProductAlias).filter(ProductAlias.product_id == item.id).delete()
    for a in item.aliases:
        db.add(ProductAlias(id=f"{item.id}-alias-{a}", product_id=item.id, alias_text=a))

    # substitui similars
    db.query(ProductSimilar).filter(ProductSimilar.product_id == item.id).delete()
    for spid in item.similar_product_ids:
        db.add(ProductSimilar(id=f"{item.id}-sim-{spid}", product_id=item.id, similar_product_id=spid))

def upsert_vehicle(db: Session, item: SeedVehicle):
    v = db.query(Vehicle).filter(Vehicle.id == item.id).first()
    if not v:
        v = Vehicle(**item.model_dump())
        db.add(v)
    else:
        for k, val in item.model_dump().items():
            setattr(v, k, val)

def upsert_company(db: Session, item: SeedCompany):
    c = db.query(Company).filter(Company.id == item.id).first()
    if not c:
        c = Company(**item.model_dump())
        db.add(c)
    else:
        for k, val in item.model_dump().items():
            setattr(c, k, val)

def upsert_company_product(db: Session, item: SeedCompanyProduct):
    cp = db.query(CompanyProduct).filter(CompanyProduct.id == item.id).first()
    if not cp:
        cp = CompanyProduct(**item.model_dump())
        db.add(cp)
    else:
        for k, val in item.model_dump().items():
            setattr(cp, k, val)

def upsert_tax(db: Session, item: SeedTax):
    t = db.query(CompanyProductTax).filter(CompanyProductTax.id == item.id).first()
    if not t:
        t = CompanyProductTax(**item.model_dump())
        db.add(t)
    else:
        for k, val in item.model_dump().items():
            setattr(t, k, val)

# ---------
# Endpoint
# ---------
@router.post("/full")
def seed_full(payload: SeedPayload, db: Session = Depends(get_db)):
    try:
        created = {
            "products": 0,
            "vehicles": 0,
            "applications": 0,
            "company": 0,
            "company_products": 0,
            "taxes": 0,
        }
        updated = created.copy()

        # company
        if payload.company:
            existed = db.query(Company).filter(Company.id == payload.company.id).first()
            upsert_company(db, payload.company)
            if existed:
                updated["company"] += 1
            else:
                created["company"] += 1

        # products
        for item in payload.products:
            existed = db.query(Product).filter(Product.id == item.id).first()
            upsert_product(db, item)
            if existed:
                updated["products"] += 1
            else:
                created["products"] += 1

        # vehicles
        for item in payload.vehicles:
            existed = db.query(Vehicle).filter(Vehicle.id == item.id).first()
            upsert_vehicle(db, item)
            if existed:
                updated["vehicles"] += 1
            else:
                created["vehicles"] += 1

        db.flush()

        # applications (idempotente por id)
        for item in payload.applications:
            existed = db.query(Application).filter(Application.id == item.id).first()
            if not existed:
                # valida FK
                p = db.query(Product).filter(Product.id == item.product_id).first()
                v = db.query(Vehicle).filter(Vehicle.id == item.vehicle_id).first()
                if not p or not v:
                    continue
                db.add(Application(**item.model_dump()))
                created["applications"] += 1
            else:
                existed.observacoes = item.observacoes
                updated["applications"] += 1

        # company_products
        for item in payload.company_products:
            existed = db.query(CompanyProduct).filter(CompanyProduct.id == item.id).first()
            upsert_company_product(db, item)
            if existed:
                updated["company_products"] += 1
            else:
                created["company_products"] += 1

        # taxes
        for item in payload.taxes:
            existed = db.query(CompanyProductTax).filter(CompanyProductTax.id == item.id).first()
            upsert_tax(db, item)
            if existed:
                updated["taxes"] += 1
            else:
                created["taxes"] += 1

        db.commit()
        return {"ok": True, "created": created, "updated": updated}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
