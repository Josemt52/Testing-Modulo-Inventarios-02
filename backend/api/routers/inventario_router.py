from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.inventario import MovimientoInventarioIn
from api.services import inventario_service

router = APIRouter(prefix="/inventario", tags=["Inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/entrada")
def registrar_entrada(data: MovimientoInventarioIn, db: Session = Depends(get_db)):
    if data.tipo != "entrada":
        raise HTTPException(status_code=400, detail="Este endpoint es solo para entradas")
    return inventario_service.procesar_movimiento(db, data)

@router.post("/salida")
def registrar_salida(data: MovimientoInventarioIn, db: Session = Depends(get_db)):
    if data.tipo != "salida":
        raise HTTPException(status_code=400, detail="Este endpoint es solo para salidas")
    return inventario_service.procesar_movimiento(db, data)
