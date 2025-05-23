from pydantic import BaseModel, Field

class CategoriaCreate(BaseModel):
    nombre: str

class CategoriaOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=1)