from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.almacen import Almacen
from api.schemas.almacen import AlmacenCreate, AlmacenOut

router = APIRouter(prefix="/almacenes", tags=["Almacenes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AlmacenOut)
def crear_almacen(data: AlmacenCreate, db: Session = Depends(get_db)):
    almacen = Almacen(**data.dict())
    db.add(almacen)
    db.commit()
    db.refresh(almacen)
    return almacen

@router.get("/", response_model=list[AlmacenOut])
def listar_almacenes(db: Session = Depends(get_db)):
    return db.query(Almacen).all()
