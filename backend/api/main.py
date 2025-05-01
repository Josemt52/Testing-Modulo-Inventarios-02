from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import producto_router, inventario_router, auth_router
from api.database import Base, engine

from api.models import producto, categoria, marca, usuario, movimiento

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Inventario")

app.include_router(auth_router.router)
app.include_router(producto_router.router)
app.include_router(inventario_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/test")
def test_endpoint():
    return {"message": "Hello from FastAPI!"}