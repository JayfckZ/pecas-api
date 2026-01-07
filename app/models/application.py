from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from .base import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)
    vehicle_id = Column(String, ForeignKey("vehicles.id"), nullable=False, index=True)
    observacoes = Column(Text, nullable=True)

    product = relationship("Product", back_populates="applications")
    vehicle = relationship("Vehicle", back_populates="applications")
