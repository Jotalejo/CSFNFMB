from pydantic import BaseModel
from typing import Optional
		
class ResiduosCliBase(BaseModel):
    ccliente: int
    tresiduo: int
    cantresiduo: float
    pesopromres: float
    segregares: Optional[str] = None
    numbolsas: Optional[int] = None
    observaciones: Optional[str] = None
		
class ResiduosCliCreate(ResiduosCliBase):
    pass
		
class ResiduosCliUpdate(ResiduosCliBase):
    id: int
		
class ResiduosCliOut(ResiduosCliBase):
    id: int
		
    class Config:
        orm_mode = True