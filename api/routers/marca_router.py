from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.marca import Marca
from api.schemas.marca import MarcaCreate, MarcaOut
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/marcas", tags=["Marcas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MarcaOut)
def crear_marca(data: MarcaCreate, db: Session = Depends(get_db)):
    existente = db.query(Marca).filter(Marca.nombre == data.nombre, Marca.activo == True).first()
    if existente:
        raise HTTPException(status_code=409, detail="La marca ya existe.")

    try:
        nueva = Marca(**data.model_dump())
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto con marca existente")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al crear marca")

@router.get("/", response_model=list[MarcaOut])
def listar_marcas(db: Session = Depends(get_db)):
    # Solo marcas activas
    return db.query(Marca).filter(Marca.activo == True).all()

@router.put("/{id}", response_model=MarcaOut)
def actualizar_marca(id: int, data: MarcaCreate, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == id, Marca.activo == True).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Validar que no haya otra marca activa con el mismo nombre
    otra_marca = db.query(Marca).filter(
        Marca.nombre == data.nombre,
        Marca.id != id,
        Marca.activo == True
    ).first()
    if otra_marca:
        raise HTTPException(status_code=409, detail="Ya existe otra marca con ese nombre")

    try:
        marca.nombre = data.nombre
        db.commit()
        db.refresh(marca)
        return marca
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al actualizar marca")
    
@router.delete("/{id}")
def eliminar_marca(id: int, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == id, Marca.activo == True).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    try:
        marca.activo = False  # borrado lógico
        db.commit()
        return {"detail": "Marca eliminada correctamente"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al eliminar marca")
