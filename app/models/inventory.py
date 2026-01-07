from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Integer, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

def now_utc():
    return datetime.utcnow()

class CompanyProduct(Base):
    __tablename__ = "company_products"

    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)

    ativo = Column(Boolean, default=True)

    preco_venda = Column(Float, default=0.0)
    preco_custo = Column(Float, default=0.0)

    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=0)

    localizacao = Column(Text, nullable=True)

    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    company = relationship("Company", back_populates="company_products")
    product = relationship("Product")

    movements = relationship("InventoryMovement", back_populates="company_product", cascade="all, delete-orphan")


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)
    company_product_id = Column(String, ForeignKey("company_products.id"), nullable=False, index=True)

    tipo = Column(String, nullable=False)  # IN | OUT | AJUSTE
    quantidade = Column(Integer, nullable=False)
    custo_unitario = Column(Float, nullable=True)
    origem = Column(String, nullable=True)  # venda, compra, ajuste manual
    observacoes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=now_utc)

    company_product = relationship("CompanyProduct", back_populates="movements")
