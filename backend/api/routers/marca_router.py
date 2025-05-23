from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.marca import Marca
from api.schemas.marca import MarcaCreate, MarcaOut

router = APIRouter(prefix="/marcas", tags=["Marcas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MarcaOut)
def crear_marca(data: MarcaCreate, db: Session = Depends(get_db)):
    existente = db.query(Marca).filter(Marca.nombre == data.nombre).first()
    if existente:
        return existente
    nueva = Marca(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[MarcaOut])
def listar_marcas(db: Session = Depends(get_db)):
    return db.query(Marca).all()