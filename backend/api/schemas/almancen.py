from pydantic import BaseModel

class AlmacenCreate(BaseModel):
    nombre: str
    ubicacion: str

class AlmacenOut(AlmacenCreate):
    id: int

    class Config:
        from_attributes = True