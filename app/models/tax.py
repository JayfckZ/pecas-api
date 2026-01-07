from sqlalchemy import Column, String, ForeignKey, Float, Text
from .base import Base

class CompanyProductTax(Base):
    __tablename__ = "company_product_tax"

    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)

    ncm = Column(String, nullable=True, index=True)
    cest = Column(String, nullable=True, index=True)
    cfop_saida_padrao = Column(String, nullable=True)
    origem_mercadoria = Column(String, nullable=True)

    cst_icms = Column(String, nullable=True)
    csosn = Column(String, nullable=True)

    aliquota_icms = Column(Float, nullable=True)
    aliquota_pis = Column(Float, nullable=True)
    aliquota_cofins = Column(Float, nullable=True)

    observacoes = Column(Text, nullable=True)
