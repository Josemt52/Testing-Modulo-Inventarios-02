from fastapi import APIRouter, Depends, HTTPException
from scipy import stats
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.movimiento import MovimientoInventario
from api.schemas.movimiento import MovimientoCreate, MovimientoOut

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from api.models.producto import Producto

@router.post("/", response_model=MovimientoOut)
def crear_movimiento(data: MovimientoCreate, db: Session = Depends(get_db)):
    if not db.query(Producto).filter(Producto.id == data.producto_id).first():
        raise HTTPException(status_code=400, detail="Producto no existe")
    movimiento = MovimientoInventario(**data.dict())
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento


@router.get("/", response_model=list[MovimientoOut])
def listar_movimientos(db: Session = Depends(get_db)):
    return db.query(MovimientoInventario).filter(MovimientoInventario.cantidad > 0).all()
