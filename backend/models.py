from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import  Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Financa(Base):
    __tablename__ = "financa"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    type_input = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now())
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="financas")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    financas = relationship("Financa", back_populates="category", cascade="all, delete")