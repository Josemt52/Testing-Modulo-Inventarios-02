from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.producto import ProductoCreate, ProductoOut, ProductoUpdate
from api.services import producto_service
from api.repositories import producto_repository
from api.models.producto import Producto
from api.models.movimiento import MovimientoInventario

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductoOut)
def crear(data: ProductoCreate, db: Session = Depends(get_db)):
    return producto_service.crear_producto(db, data)


@router.get("/", response_model=list[ProductoOut])
def listar(db: Session = Depends(get_db)):
    return producto_repository.obtener_todos(db)


@router.put("/{producto_id}", response_model=ProductoOut)
def actualizar(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)):
    actualizado = producto_service.actualizar_producto(db, producto_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return actualizado

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar si hay movimientos asociados
    movimientos = db.query(MovimientoInventario).filter(MovimientoInventario.producto_id == producto_id).count()
    if movimientos > 0:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el producto porque tiene movimientos registrados"
        )

    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado correctamente"}
