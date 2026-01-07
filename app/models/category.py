from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

    subcategories = relationship("Subcategory", back_populates="category", cascade="all, delete-orphan")


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(String, primary_key=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    nome = Column(String, nullable=False)

    category = relationship("Category", back_populates="subcategories")
