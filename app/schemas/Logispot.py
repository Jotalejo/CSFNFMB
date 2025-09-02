# schemas/Logispot.py
from pydantic import BaseModel
from typing import Optional

# Base (sin id)
class Logispot(BaseModel):
    codclipot: Optional[int] = None
    frecuerec: Optional[str] = None
    capavehic: Optional[str] = None
    distancia: Optional[float] = None
    observaciones: Optional[str] = None

    @classmethod
    def from_dictLogp(cls, data: dict):
        return cls(**data)

# Create
class LogiPotCreate(Logispot):
    pass

# Output / Update (con id)
class LogiPotOut(Logispot):
    id: int
    class Config:
        from_attributes = True  # (si usas Pydantic v1, usa: orm_mode = True)
