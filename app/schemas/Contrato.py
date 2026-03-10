from pydantic import BaseModel
from datetime import date
from typing import Optional

class ContratoCreate(BaseModel):
    fecha_inicio: date
    lugar_ejecucion: str
    rep_nombre: str
    rep_cc: str
    rep_exp_lugar: str
    fecha_firma: date
    mes_actual: Optional[str] = None

class ContratoOut(BaseModel):
    id: int
    cliente_id: int
    fecha_inicio: date
    fecha_fin: date
    lugar_ejecucion: str
    rep_nombre: str
    rep_cc: str
    rep_exp_lugar: str
    fecha_firma: date
    mes_actual: str
    docx_path: Optional[str] = None
    pdf_path: Optional[str] = None

    class Config:
        from_attributes = True