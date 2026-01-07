from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Company
from app.schemas.company import CompanyCreate, CompanyOut

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("", response_model=CompanyOut)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    c = Company(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return CompanyOut(**payload.model_dump())

@router.get("", response_model=list[CompanyOut])
def list_companies(q: str | None = Query(None), limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(Company)
    if q:
        like = f"%{q}%"
        query = query.filter(Company.nome.like(like))
    items = query.order_by(Company.nome.asc()).limit(limit).all()
    return [
        CompanyOut(
            id=c.id,
            nome=c.nome,
            cnpj=c.cnpj,
            ativo=c.ativo
        )
        for c in items
    ]

@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: str, db: Session = Depends(get_db)):
    c = db.query(Company).filter(Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return CompanyOut(
        id=c.id,
        nome=c.nome,
        cnpj=c.cnpj,
        ativo=c.ativo
    )
