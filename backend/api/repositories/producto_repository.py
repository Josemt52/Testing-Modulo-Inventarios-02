from sqlalchemy.orm import Session
from api.models.producto import Producto

def obtener_todos(db: Session):
    return db.query(Producto).all()

def obtener_por_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def crear_producto(db: Session, producto: Producto):
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

def actualizar_producto(db: Session, db_producto: Producto, cambios: dict):
    for key, value in cambios.items():
        setattr(db_producto, key, value)
    db.commit()
    return db_producto

def eliminar_producto(db: Session, producto: Producto):
    db.delete(producto)
    db.commit()
