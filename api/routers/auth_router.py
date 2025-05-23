# api/routers/auth_router.py (agrega import y endpoint nuevo)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.usuario import UsuarioLogin, UsuarioRegistro
from api.services.usuario_service import verificar_usuario, encriptar_password
from api.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = verificar_usuario(db, usuario.email, usuario.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    hashed_password = encriptar_password(usuario.password)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        rol=usuario.rol,
        email=usuario.email,
        password=hashed_password
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "rol": nuevo_usuario.rol,
        "email": nuevo_usuario.email,
    }
