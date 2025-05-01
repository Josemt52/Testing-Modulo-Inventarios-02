from sqlalchemy.orm import Session
from api.models.movimiento import MovimientoInventario
from api.models.producto import Producto

def registrar_movimiento(db: Session, movimiento: MovimientoInventario):
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento

def actualizar_stock(db: Session, producto_id: int, cantidad: int, tipo: str):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto:
        if tipo == 'entrada':
            producto.stock_actual += cantidad
        elif tipo == 'salida':
            producto.stock_actual -= cantidad
        db.commit()
    return producto

def obtener_todos(db: Session):
    return db.query(MovimientoInventario).all()