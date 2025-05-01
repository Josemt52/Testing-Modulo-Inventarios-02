from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TipoMovimiento(str, Enum):
    entrada = 'entrada'
    salida = 'salida'

class MovimientoInventarioIn(BaseModel):
    producto_id: int
    tipo: TipoMovimiento
    cantidad: int
    almacen_id: Optional[int]
    origen: Optional[str]
    observaciones: Optional[str]
    
class Config:
    from_attributes = True