from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models.categoria import Categoria
from api.schemas.categoria import CategoriaCreate, CategoriaOut, CategoriaUpdate

router = APIRouter(prefix="/categorias", tags=["Categorías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoriaOut)
def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):
    existente = db.query(Categoria).filter(Categoria.nombre == data.nombre).first()
    if existente:
        raise HTTPException(status_code=409, detail="La categoría ya existe.")

    nueva = Categoria(**data.model_dump())
    try:
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto con categoría existente")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al crear categoría")

@router.get("/", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).filter(Categoria.activo == True).all()

@router.put("/{categoria_id}", response_model=CategoriaOut)
def actualizar_categoria(categoria_id: int, data: CategoriaCreate, db: Session = Depends(get_db)):
    # Buscar la categoria activa por ID
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id, Categoria.activo == True).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o inactiva")

    # Verificar que no exista otra categoria activa con el nuevo nombre
    existe_nombre = db.query(Categoria).filter(
        Categoria.nombre == data.nombre,
        Categoria.id != categoria_id,
        Categoria.activo == True
    ).first()
    if existe_nombre:
        raise HTTPException(status_code=400, detail="Ya existe una categoría activa con ese nombre")

    # Actualizar el nombre
    categoria.nombre = data.nombre

    db.commit()
    db.refresh(categoria)
    return categoria

    
@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id, Categoria.activo == True).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o ya eliminada")

    categoria.activo = False  # Aquí cambia el estado en lugar de eliminar
    db.commit()
    return
