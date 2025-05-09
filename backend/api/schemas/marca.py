from pydantic import BaseModel, Field

class MarcaCreate(BaseModel):
    nombre: str = Field(..., min_length=1)

class MarcaOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True