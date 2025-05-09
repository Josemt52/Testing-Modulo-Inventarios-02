from pydantic import BaseModel

class UsuarioLogin(BaseModel):
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    rol: str
    email: str

    class Config:
        from_attributes = True  