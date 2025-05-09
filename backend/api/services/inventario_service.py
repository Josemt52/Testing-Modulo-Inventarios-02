from sqlalchemy.orm import Session
from api.schemas.inventario import MovimientoInventarioIn
from api.models.movimiento import MovimientoInventario
from api.repositories import inventario_repository

def procesar_movimiento(db: Session, data: MovimientoInventarioIn):
    movimiento = MovimientoInventario(**data.dict())
    inventario_repository.registrar_movimiento(db, movimiento)
    producto_actualizado = inventario_repository.actualizar_stock(
        db, data.producto_id, data.cantidad, data.tipo
    )
    return producto_actualizado
