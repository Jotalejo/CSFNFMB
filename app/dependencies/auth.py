from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from config import get_settings, Settings
from sqlalchemy.orm import Session
from .database import get_db


def get_current_user_from_request(request: Request, db: Session, settings: Settings):
    """Versión interna sin Depends() para uso en middlewares y funciones auxiliares"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email = payload["sub"]

        # Importar aquí para evitar importación circular
        from models.User import Usuario
        user = db.query(Usuario).filter(Usuario.email == email).first()
        return user
    except JWTError:
        return None


def get_current_user(request: Request, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    """Versión para usar en endpoints de FastAPI con inyección de dependencias"""
    return get_current_user_from_request(request, db, settings)
