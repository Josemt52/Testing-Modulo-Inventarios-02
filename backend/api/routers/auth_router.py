from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.usuario import UsuarioLogin, UsuarioOut
from api.services.usuario_service import verificar_usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=UsuarioOut)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    user = verificar_usuario(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return user
