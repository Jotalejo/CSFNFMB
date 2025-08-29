from pydantic import BaseModel
import datetime

class CrearUsuario(BaseModel):
    nombre: str
    email: str
    password: str

class CrearToken(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool = True
    created_at: datetime.datetime = datetime.datetime.now()

class RequestDetails(BaseModel):
    email: str
    password: str

class ResetPassword(BaseModel):
    email: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class CambiarPassword(BaseModel):
    email: str
    old_password: str
    new_password: str
