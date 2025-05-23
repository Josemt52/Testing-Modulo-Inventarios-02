from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.producto import ProductoCreate, ProductoUpdate
from api.services import producto_service
from api.models.producto import Producto 
from pydantic import BaseModel

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/todos")
def listar_productos(db: Session = Depends(get_db)):
    return producto_service.obtener_productos(db)

@router.post("/")
def crear_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    try:
        return producto_service.crear_producto(db, data)
    except Exception:
        raise HTTPException(status_code=500, detail="Error al crear producto")

@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)):
    producto = producto_service.actualizar_producto(db, producto_id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = producto_service.eliminar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

class ProductoSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

@router.get("/todos_incluye_inactivos", response_model=list[ProductoSimple])
def listar_todos_productos_incluye_inactivos(db: Session = Depends(get_db)):
    productos = db.query(Producto).order_by(Producto.nombre).all()
    return productos