from sqlalchemy.orm import Session
from api.schemas.producto import ProductoCreate, ProductoUpdate
from api.models.producto import Producto
from api.repositories import producto_repository

def crear_producto(db: Session, data: ProductoCreate):
    producto = Producto(**data.dict())
    return producto_repository.crear_producto(db, producto)

def actualizar_producto(db: Session, producto_id: int, data: ProductoUpdate):
    db_producto = producto_repository.obtener_por_id(db, producto_id)
    if not db_producto:
        return None
    return producto_repository.actualizar_producto(db, db_producto, data.dict())
