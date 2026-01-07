from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Application, Product, Vehicle
from app.schemas.application import ApplicationCreate, ApplicationOut

router = APIRouter(prefix="/catalog/applications", tags=["Catalog - Applications"])

@router.post("", response_model=ApplicationOut)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == payload.product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    v = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    a = Application(**payload.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return ApplicationOut(**payload.model_dump())

@router.get("", response_model=list[ApplicationOut])
def list_applications(
    product_id: str | None = Query(None),
    vehicle_id: str | None = Query(None),
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Application)

    if product_id:
        query = query.filter(Application.product_id == product_id)

    if vehicle_id:
        query = query.filter(Application.vehicle_id == vehicle_id)

    items = query.order_by(Application.id.asc()).limit(limit).all()

    return [
        ApplicationOut(
            id=a.id,
            product_id=a.product_id,
            vehicle_id=a.vehicle_id,
            observacoes=a.observacoes
        )
        for a in items
    ]

@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(application_id: str, db: Session = Depends(get_db)):
    a = db.query(Application).filter(Application.id == application_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Aplicação não encontrada")

    return ApplicationOut(
        id=a.id,
        product_id=a.product_id,
        vehicle_id=a.vehicle_id,
        observacoes=a.observacoes
    )
