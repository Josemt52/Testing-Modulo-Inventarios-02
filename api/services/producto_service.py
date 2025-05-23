from sqlalchemy.orm import Session
from api.schemas.producto import ProductoCreate, ProductoUpdate
from api.models.producto import Producto
from api.models.categoria import Categoria
from api.models.marca import Marca
from api.repositories import producto_repository


from fastapi import HTTPException

def crear_producto(db: Session, data: ProductoCreate):
    try:
        # Verificar si ya existe un producto con el mismo nombre y activo
        producto_existente = db.query(Producto).filter(
            Producto.nombre == data.nombre,
            Producto.activo == True
        ).first()

        if producto_existente:
            raise HTTPException(status_code=400, detail="El producto ya existe y está activo.")

        # Crear el producto si no existe activo
        producto = Producto(**data.model_dump())
        return producto_repository.crear_producto(db, producto)

    except HTTPException as e:
        # Re-lanza para que FastAPI lo capture y muestre bien
        raise e
    except Exception as e:
        # Captura otros errores y devuelve un error 500 con mensaje claro
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


from fastapi import HTTPException

def actualizar_producto(db: Session, producto_id: int, data: ProductoUpdate):
    producto = db.query(Producto).filter(Producto.id == producto_id, Producto.activo == True).first()
    if not producto:
        return None

    if hasattr(data, "stock_actual") and data.stock_actual is not None and data.stock_actual != producto.stock_actual:
        raise HTTPException(status_code=400, detail="No se puede actualizar el stock actual directamente")

    if data.nombre and data.nombre != producto.nombre:
        producto_existente = db.query(Producto).filter(
            Producto.nombre == data.nombre,
            Producto.activo == True,
            Producto.id != producto_id
        ).first()
        if producto_existente:
            raise HTTPException(status_code=400, detail="Ya existe un producto activo con ese nombre")

    data_dict = data.model_dump()
    data_dict['stock_actual'] = producto.stock_actual

    for key, value in data_dict.items():
        setattr(producto, key, value)

    db.commit()
    db.refresh(producto)

    # Obtener nombres de categoria y marca para devolverlos junto al producto actualizado
    categoria_nombre = None
    marca_nombre = None
    if producto.categoria_id:
        categoria = db.query(Categoria).filter(Categoria.id == producto.categoria_id).first()
        categoria_nombre = categoria.nombre if categoria else None
    if producto.marca_id:
        marca = db.query(Marca).filter(Marca.id == producto.marca_id).first()
        marca_nombre = marca.nombre if marca else None

    producto_dict = producto.__dict__.copy()
    producto_dict["categoria_nombre"] = categoria_nombre
    producto_dict["marca_nombre"] = marca_nombre
    producto_dict.pop('_sa_instance_state', None)  # Eliminar campo no serializable

    return producto_dict



def obtener_productos(db: Session):
    # Consulta con joins para traer nombre de categoria y marca,
    # pero solo productos activos
    productos = (
    db.query(
        Producto,
        Categoria.nombre.label("categoria_nombre"),
        Marca.nombre.label("marca_nombre"),
    )
    .join(Categoria, Producto.categoria_id == Categoria.id)
    .join(Marca, Producto.marca_id == Marca.id)
    .filter(Producto.activo == '1')
    .all()
    )

    print(productos)

    lista = []
    for prod, cat_nombre, mar_nombre in productos:
        p = prod.__dict__.copy()
        p["categoria_nombre"] = cat_nombre
        p["marca_nombre"] = mar_nombre
        # Opcional: eliminar el campo 'activo' del dict para no mostrarlo
        p.pop('activo', None)
        lista.append(p)
    return lista


def eliminar_producto(db: Session, producto_id: int):
    
    return producto_repository.eliminar_producto(db, producto_id)
