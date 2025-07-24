from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FinancaSchema(BaseModel):
    id: int
    name: str
    value: float
    type_input: str
    created_at: datetime
    description: str
    category_id: int

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str
    financa: Optional[List[FinancaSchema]] = None

    class Config:
        orm_mode = True
