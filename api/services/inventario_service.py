from sqlalchemy.orm import Session
from api.schemas.inventario import MovimientoInventarioIn
from api.models.movimiento import MovimientoInventario
from api.repositories import inventario_repository
from sqlalchemy import func
from api.models.movimiento import MovimientoInventario, TipoMovimientoEnum

def procesar_movimiento(db: Session, data: MovimientoInventarioIn):
    # Validar stock si es una salida
    if data.tipo == "salida":
        entradas = db.query(func.sum(MovimientoInventario.cantidad)).filter(
            MovimientoInventario.producto_id == data.producto_id,
            MovimientoInventario.tipo == TipoMovimientoEnum.entrada,
            MovimientoInventario.almacen_id == data.almacen_id
        ).scalar() or 0

        salidas = db.query(func.sum(MovimientoInventario.cantidad)).filter(
            MovimientoInventario.producto_id == data.producto_id,
            MovimientoInventario.tipo == TipoMovimientoEnum.salida,
            MovimientoInventario.almacen_id == data.almacen_id
        ).scalar() or 0

        stock_actual = entradas - salidas
        if data.cantidad > stock_actual:
            raise ValueError(f"Stock insuficiente. Stock actual: {stock_actual}, solicitado: {data.cantidad}")

    # Validar que almacén y origen no sean el mismo (si aplica)
    if data.origen and data.origen.strip() != "" and str(data.origen).isdigit():
        if int(data.origen) == data.almacen_id:
            raise ValueError("El almacén de origen y destino no pueden ser el mismo.")

    # Registrar el movimiento
    movimiento = MovimientoInventario(**data.model_dump())
    return inventario_repository.registrar_movimiento(db, movimiento)
