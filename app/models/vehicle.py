from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True)
    montadora = Column(String, nullable=False, index=True)
    modelo = Column(String, nullable=False, index=True)
    ano = Column(Integer, nullable=False, index=True)
    motor = Column(String, nullable=True, index=True)
    versao = Column(String, nullable=True)
    texto_busca = Column(Text, nullable=True)

    applications = relationship("Application", back_populates="vehicle", cascade="all, delete-orphan")
