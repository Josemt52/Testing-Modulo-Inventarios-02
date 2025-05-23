from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.almacen import Almacen
from api.schemas.almacen import AlmacenCreate, AlmacenOut
from api.models.almacen import Almacen
from pydantic import BaseModel

router = APIRouter(prefix="/almacenes", tags=["Almacenes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AlmacenOut)
def crear_almacen(data: AlmacenCreate, db: Session = Depends(get_db)):
    existente = db.query(Almacen).filter(Almacen.nombre == data.nombre, Almacen.activo == True).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un almacén activo con ese nombre")
    
    nuevo = Almacen(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[AlmacenOut])
def listar_almacenes(db: Session = Depends(get_db)):
    return db.query(Almacen).filter(Almacen.activo == True).all()

@router.put("/{almacen_id}", response_model=AlmacenOut)
def actualizar_almacen(almacen_id: int, data: AlmacenCreate, db: Session = Depends(get_db)):
    almacen = db.query(Almacen).filter(Almacen.id == almacen_id).first()
    if not almacen or not almacen.activo:
        raise HTTPException(status_code=404, detail="Almacén no encontrado o inactivo")

    duplicado = db.query(Almacen).filter(Almacen.nombre == data.nombre, Almacen.id != almacen_id, Almacen.activo == True).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Ya existe otro almacén activo con ese nombre")

    almacen.nombre = data.nombre
    almacen.ubicacion = data.ubicacion
    db.commit()
    db.refresh(almacen)
    return almacen

@router.delete("/{almacen_id}")
def eliminar_almacen(almacen_id: int, db: Session = Depends(get_db)):
    almacen = db.query(Almacen).filter(Almacen.id == almacen_id).first()
    if not almacen or not almacen.activo:
        raise HTTPException(status_code=404, detail="Almacén no encontrado o ya inactivo")
    
    almacen.activo = False
    db.commit()
    return {"mensaje": "Almacén desactivado correctamente"}

class AlmacenSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

@router.get("/todos_incluye_inactivos", response_model=list[AlmacenSimple])
def listar_todos_almacenes_incluye_inactivos(db: Session = Depends(get_db)):
    almacenes = db.query(Almacen).order_by(Almacen.nombre).all()
    return almacenes