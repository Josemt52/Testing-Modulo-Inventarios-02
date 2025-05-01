from fastapi import FastAPI
from api.routers import producto_router, inventario_router, auth_router
from api.database import Base, engine

from api.models import producto, categoria, marca, usuario, movimiento

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Inventario")

app.include_router(auth_router.router)
app.include_router(producto_router.router)
app.include_router(inventario_router.router)
