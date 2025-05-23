from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.schemas.producto import ProductoCreate, ProductoOut, ProductoUpdate
from api.services import producto_service
from api.repositories import producto_repository

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
