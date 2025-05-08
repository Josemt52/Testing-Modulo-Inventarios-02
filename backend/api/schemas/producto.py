from pydantic import BaseModel, Field
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    categoria_id: Optional[int] = None
    marca_id: Optional[int] = None
    precio: float
    stock_actual: int
    stock_minimo: int
    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int

    class Config:
        from_attributes = True
        
class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    precio: float = Field(..., gt=0)
    stock_actual: int
    stock_minimo: int
    activo: bool