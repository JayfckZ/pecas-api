from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Company, Product, CompanyProduct
from app.schemas.inventory import CompanyProductCreate, CompanyProductOut

router = APIRouter(prefix="/pdv/company-products", tags=["PDV - Company Products"])

@router.post("", response_model=CompanyProductOut)
def enable_product(payload: CompanyProductCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    cp = CompanyProduct(**payload.model_dump())
    db.add(cp)
    db.commit()
    db.refresh(cp)
    return CompanyProductOut(**payload.model_dump())
