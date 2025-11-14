from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from services.logistica_service import LogisticaService
from pydantic import BaseModel
from typing import Optional, Any

router = APIRouter(
    prefix="/logistica",
    tags=["logistica"],
    dependencies=[Depends(get_db)],
)

class LogisticaIn(BaseModel):
    frecuencia_resumen: str
    capacidad_kg: Optional[int] = None
    configuracion: Optional[dict[str, Any]] = None  # se serializa a JSON

@router.post("/cliente/{cliente_id}")
def upsert_logistica(cliente_id: int, data: LogisticaIn, db: Session = Depends(get_db)):
    svc = LogisticaService(db)
    row = svc.upsert_for_cliente(
        cliente_id=cliente_id,
        frecuencia=data.frecuencia_resumen,
        capacidad=data.capacidad_kg,
        observ_json=data.configuracion,
    )
    if not row:
        raise HTTPException(status_code=500, detail="No se pudo guardar")
    return {"ok": True, "id": row.id}
