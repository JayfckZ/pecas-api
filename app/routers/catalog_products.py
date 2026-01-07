from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Product, ProductAlias, ProductSimilar
from app.schemas.product import ProductCreate, ProductOut

router = APIRouter(prefix="/catalog/products", tags=["Catalog - Products"])

def to_out(p: Product) -> ProductOut:
    return ProductOut(
        id=p.id,
        codigo_interno=p.codigo_interno,
        descricao_principal=p.descricao_principal,
        marca=p.marca,
        unidade=p.unidade,
        ean=p.ean,
        codigo_fabricante=p.codigo_fabricante,
        imagem_url=p.imagem_url,
        category_id=p.category_id,
        subcategory_id=p.subcategory_id,
        ativo=p.ativo,
        aliases=[a.alias_text for a in p.aliases],
        similar_product_ids=[s.similar_product_id for s in p.similars],
    )

@router.post("", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    exists = db.query(Product).filter(Product.codigo_interno == payload.codigo_interno).first()
    if exists:
        raise HTTPException(status_code=409, detail="Já existe produto com esse codigo_interno")

    p = Product(
        id=payload.id,
        codigo_interno=payload.codigo_interno,
        descricao_principal=payload.descricao_principal,
        marca=payload.marca,
        unidade=payload.unidade,
        ean=payload.ean,
        codigo_fabricante=payload.codigo_fabricante,
        imagem_url=payload.imagem_url,
        category_id=payload.category_id,
        subcategory_id=payload.subcategory_id,
        ativo=payload.ativo,
    )

    for a in payload.aliases:
        p.aliases.append(ProductAlias(id=f"{payload.id}-alias-{a}", alias_text=a))

    for spid in payload.similar_product_ids:
        p.similars.append(ProductSimilar(id=f"{payload.id}-sim-{spid}", similar_product_id=spid))

    db.add(p)
    db.commit()
    db.refresh(p)
    return to_out(p)

@router.get("", response_model=list[ProductOut])
def list_products(
    q: str | None = Query(None),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (Product.codigo_interno.like(like)) |
            (Product.descricao_principal.like(like)) |
            (Product.marca.like(like)) |
            (Product.ean.like(like)) |
            (Product.codigo_fabricante.like(like))
        )

    items = query.order_by(Product.updated_at.desc()).limit(limit).all()
    return [to_out(p) for p in items]

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return to_out(p)
