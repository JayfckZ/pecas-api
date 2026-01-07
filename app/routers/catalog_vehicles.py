from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleOut

router = APIRouter(prefix="/catalog/vehicles", tags=["Catalog - Vehicles"])

@router.post("", response_model=VehicleOut)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    exists = db.query(Vehicle).filter(
        Vehicle.montadora == payload.montadora,
        Vehicle.modelo == payload.modelo,
        Vehicle.ano == payload.ano,
        Vehicle.motor == payload.motor
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="Veículo já existe nesse catálogo")

    v = Vehicle(**payload.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    return VehicleOut(**payload.model_dump())

@router.get("", response_model=list[VehicleOut])
def list_vehicles(
    q: str | None = Query(None),
    montadora: str | None = Query(None),
    modelo: str | None = Query(None),
    ano: int | None = Query(None),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Vehicle)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (Vehicle.montadora.like(like)) |
            (Vehicle.modelo.like(like)) |
            (Vehicle.motor.like(like)) |
            (Vehicle.versao.like(like))
        )

    if montadora:
        query = query.filter(Vehicle.montadora == montadora)

    if modelo:
        query = query.filter(Vehicle.modelo == modelo)

    if ano is not None:
        query = query.filter(Vehicle.ano == ano)

    items = query.order_by(Vehicle.modelo.asc(), Vehicle.ano.asc()).limit(limit).all()

    return [
        VehicleOut(
            id=v.id,
            montadora=v.montadora,
            modelo=v.modelo,
            ano=v.ano,
            motor=v.motor,
            versao=v.versao,
            texto_busca=v.texto_busca
        )
        for v in items
    ]

@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    v = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    return VehicleOut(
        id=v.id,
        montadora=v.montadora,
        modelo=v.modelo,
        ano=v.ano,
        motor=v.motor,
        versao=v.versao,
        texto_busca=v.texto_busca
    )
