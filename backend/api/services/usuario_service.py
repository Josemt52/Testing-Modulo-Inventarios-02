from sqlalchemy.orm import Session
from api.models.usuario import Usuario

def verificar_usuario(db: Session, email: str, password: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user and user.password == password:
        return user
    return None
