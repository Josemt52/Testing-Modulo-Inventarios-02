from pydantic import BaseModel
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
