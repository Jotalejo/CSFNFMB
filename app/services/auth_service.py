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
import pyotp
import qrcode
import io
import base64


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

    # ============= MÉTODOS OTP =============
    
    def generate_otp_secret(self) -> str:
        """Genera un secret aleatorio para OTP"""
        return pyotp.random_base32()
    
    def get_totp_uri(self, email: str, secret: str, issuer: str = "GRESAB") -> str:
        """Genera el URI para el código QR de Google Authenticator"""
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=email,
            issuer_name=issuer
        )
    
    def generate_qr_code(self, uri: str) -> str:
        """Genera un código QR en formato base64"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer)
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    def setup_otp_for_user(self, email: str):
        """Configura OTP para un usuario"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        # Generar nuevo secret
        secret = self.generate_otp_secret()
        
        # Guardar en la base de datos
        user.otp_secret = secret
        user.otp_enabled = False  # Se activará después de verificar
        self.db.commit()
        self.db.refresh(user)
        
        # Generar URI y QR
        uri = self.get_totp_uri(email, secret)
        qr_code = self.generate_qr_code(uri)
        
        return {
            "secret": secret,
            "qr_code_url": qr_code,
            "uri": uri
        }
    
    def verify_otp(self, email: str, otp_code: str) -> bool:
        """Verifica un código OTP"""
        user = self.get_user_by_email(email)
        if not user or not user.otp_secret:
            return False
        
        totp = pyotp.TOTP(user.otp_secret)
        return totp.verify(otp_code, valid_window=1)  # valid_window=1 permite un margen de 30s
    
    def enable_otp_for_user(self, email: str, otp_code: str) -> bool:
        """Habilita OTP después de verificar el código"""
        user = self.get_user_by_email(email)
        if not user or not user.otp_secret:
            return False
        
        if self.verify_otp(email, otp_code):
            user.otp_enabled = True
            self.db.commit()
            return True
        
        return False
    
    def disable_otp_for_user(self, email: str) -> bool:
        """Deshabilita OTP para un usuario"""
        user = self.get_user_by_email(email)
        if not user:
            return False
        
        user.otp_enabled = False
        user.otp_secret = None
        self.db.commit()
        return True
