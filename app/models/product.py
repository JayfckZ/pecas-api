from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

def now_utc():
    return datetime.utcnow()

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    codigo_interno = Column(String, nullable=False, unique=True, index=True)
    descricao_principal = Column(Text, nullable=False)
    marca = Column(String, nullable=True, index=True)
    unidade = Column(String, nullable=True)  # UN, PC, KIT etc
    ean = Column(String, nullable=True, index=True)
    codigo_fabricante = Column(String, nullable=True, index=True)
    imagem_url = Column(Text, nullable=True)

    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(String, ForeignKey("subcategories.id"), nullable=True)

    ativo = Column(Boolean, default=True)

    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    aliases = relationship("ProductAlias", back_populates="product", cascade="all, delete-orphan")
    similars = relationship(
        "ProductSimilar",
        foreign_keys="ProductSimilar.product_id",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    applications = relationship("Application", back_populates="product", cascade="all, delete-orphan")


class ProductAlias(Base):
    __tablename__ = "product_aliases"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)
    alias_text = Column(String, nullable=False, index=True)

    product = relationship("Product", back_populates="aliases")


class ProductSimilar(Base):
    __tablename__ = "product_similars"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)
    similar_product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)

    product = relationship("Product", foreign_keys=[product_id], back_populates="similars")
