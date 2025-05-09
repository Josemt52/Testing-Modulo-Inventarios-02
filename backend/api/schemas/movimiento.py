from pydantic import BaseModel, Field
from typing import Literal, Optional

class MovimientoCreate(BaseModel):
    producto_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: int = Field(..., gt=0)  
    almacen_id: Optional[int] = None
    origen: Optional[str] = None
    observaciones: Optional[str] = None

class MovimientoOut(MovimientoCreate):
    id: int

    class Config:
        from_attributes = True