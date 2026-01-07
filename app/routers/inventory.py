from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import CompanyProduct, InventoryMovement
from app.schemas.inventory import InventoryMovementCreate

router = APIRouter(prefix="/pdv/inventory", tags=["PDV - Inventory"])

@router.post("/move")
def move_stock(payload: InventoryMovementCreate, db: Session = Depends(get_db)):
    cp = db.query(CompanyProduct).filter(CompanyProduct.id == payload.company_product_id).first()
    if not cp:
        raise HTTPException(status_code=404, detail="CompanyProduct não encontrado")

    if payload.tipo not in ("IN", "OUT", "AJUSTE"):
        raise HTTPException(status_code=400, detail="tipo deve ser IN, OUT ou AJUSTE")

    # atualiza estoque
    if payload.tipo == "IN":
        cp.estoque_atual += payload.quantidade
    elif payload.tipo == "OUT":
        cp.estoque_atual -= payload.quantidade
        if cp.estoque_atual < 0:
            cp.estoque_atual = 0
    else:  # AJUSTE
        cp.estoque_atual = payload.quantidade

    m = InventoryMovement(**payload.model_dump())
    db.add(m)
    db.commit()

    return {"ok": True, "estoque_atual": cp.estoque_atual}
