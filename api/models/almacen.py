from sqlalchemy import Column, Integer, String, Boolean
from api.database import Base

class Almacen(Base):
    __tablename__ = "almacenes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True) 
