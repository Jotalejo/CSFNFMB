from fastapi.templating import Jinja2Templates
from .database import get_db
from jose import jwt
from config import get_settings
from jinja2 import pass_context


@pass_context
def is_user_in_role(context, role_name: str):
    """Verifica si el usuario actual tiene un rol específico"""
    try:
        # Obtener request desde el contexto de Jinja2
        request = context.get('request')
        if not request:
            return False

        # Obtener token desde las cookies
        token = request.cookies.get("access_token")
        if not token:
            return False

        # Decodificar token
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if not email:
            return False

        # Obtener usuario de la base de datos
        from models.User import Usuario
        db = next(get_db())
        try:
            user = db.query(Usuario).filter(Usuario.email == email).first()
            if user and user.roles:
                for role in user.roles:
                    if role.name == role_name:
                        return True
        finally:
            db.close()

        return False
    except Exception:
        return False


templates = Jinja2Templates(directory="templates")
templates.env.globals['is_user_in_role'] = is_user_in_role
