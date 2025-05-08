from pydantic import BaseModel, EmailStr

class UsuarioLogin(BaseModel):
    email: EmailStr 
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    rol: str
    email: str

    class Config:
        from_attributes = True  