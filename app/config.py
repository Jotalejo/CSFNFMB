from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DB_URL: str = "sqlite:///./test.db"
    MAIL_USERNAME: str ="tu_correo"
    MAIL_PASSWORD: str ="tu_contraseña"
    MAIL_FROM: str ="tu_correo"
    MAIL_PORT: int = 587
    MAIL_SERVER: str ="smtp.tu-servidor.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool =False
    USE_CREDENTIALS: bool =True

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()