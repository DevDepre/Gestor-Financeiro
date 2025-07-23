from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import  Integer, String, Float, Text, DateTime, Enum as SQLALCHEMYENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base
from enum import Enum

class tipoEnum(Enum):
    GANHO = "Ganho"
    GASTO = "Gasto"

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=True)
    name = Column(String(100), nullable=False)

    financas = relationship("Financas", back_populates="category", cascade="all, delete")

class Financas(Base):
    __tablename__ = "financa"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=True)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    tipo = Column(Enum(tipoEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    category = relationship("Category", back_populates="financas")