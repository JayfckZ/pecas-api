from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

from .base import Base

def now_utc():
    return datetime.utcnow()

class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False, unique=True)
    cnpj = Column(String, nullable=True, index=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=now_utc)

    company_products = relationship("CompanyProduct", back_populates="company", cascade="all, delete-orphan")
