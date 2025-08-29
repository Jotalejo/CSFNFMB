from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext
from jose import jwt, JWTError
from config import get_settings, Settings
import random
import string


user_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/usuarios/login",
    scheme_name="user_oauth2")

UserTokenDep = Annotated[str, Depends(user_oauth2)]


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.settings = get_settings()

    def get_user_by_email(self, email: str) -> User.Usuario | None:
        return self.db.query(User.Usuario).filter(User.Usuario.email == email).first()

    @staticmethod
    def get_current_user(token: UserTokenDep):
        # Aquí se implementaría la lógica para decodificar el token y obtener el usuario
        # Por ejemplo, usando jwt.decode() para verificar el token y extraer los datos del usuario
        pass

    def authenticate_user(self, email: str, password: str):
        db_user = self.db.query(User.Usuario).filter(
            User.Usuario.email == email).first()
        if not db_user or not self.pwd_context.verify(password, db_user.password):
            return None
        return db_user

    def create_reset_token(self, email: str) -> str:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": email,
            "exp": expire,
            "purpose": "password_reset"
        }
        return jwt.encode(payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

    def verify_reset_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[
                                 self.settings.ALGORITHM])
            if payload.get("purpose") != "password_reset":
                return None
            return payload.get("sub")
        except JWTError:
            return None

    def generate_password(self, length: int = 8) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def update_password(self, email: str, new_password: str):
        user = self.db.query(User.Usuario).filter(
            User.Usuario.email == email).first()
        if user is None:
            return None

        hashed_password = self.pwd_context.hash(new_password)
        user.password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user
