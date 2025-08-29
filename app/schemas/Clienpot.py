# schemas/Clienpot.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Base (sin id)
class Clientespot(BaseModel):
    razonSocial: str
    nit: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[int] = None
    contacto: Optional[str] = None
    telefonoContacto: Optional[str] = None
    actividad: Optional[str] = None
    email: Optional[EmailStr] = None
    observaciones: Optional[str] = None

    @classmethod
    def from_dictClip(cls, data: dict):
        return cls(**data)

# Create : Clase para crear un cliente potencial
class CliPotCreate(Clientespot):
    pass

# Output / Update (con id)  : Cliente completo para la respuesta
class Clipot(Clientespot):
    id: int

    class Config:
        from_attributes = True   # Pydantic v2 (equiv. a orm_mode=True en v1)
