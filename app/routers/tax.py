from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import CompanyProductTax
from app.schemas.tax import CompanyProductTaxUpsert

router = APIRouter(prefix="/pdv/tax", tags=["PDV - Tax"])

@router.put("", response_model=dict)
def upsert_tax(payload: CompanyProductTaxUpsert, db: Session = Depends(get_db)):
    existing = db.query(CompanyProductTax).filter(
        CompanyProductTax.company_id == payload.company_id,
        CompanyProductTax.product_id == payload.product_id
    ).first()

    data = payload.model_dump()

    if not existing:
        t = CompanyProductTax(**data)
        db.add(t)
    else:
        for k, v in data.items():
            setattr(existing, k, v)

    db.commit()
    return {"ok": True}
