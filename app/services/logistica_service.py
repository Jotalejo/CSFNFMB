from sqlalchemy.orm import Session
from sqlalchemy import select
from models.Logistica import Logistica as LogisticaModel  # crea este modelo
import json
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from pydantic import BaseModel
from typing import Optional, Any

class LogisticaService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente(self, cliente_id: int):
        return (
            self.db.query(LogisticaModel)
            .filter(LogisticaModel.cliente_id == cliente_id)
            .first()
        )

    def upsert_for_cliente(self, cliente_id: int, frecuencia: str, capacidad: int | None, observ_json: dict | None):
        row = self.get_by_cliente(cliente_id)
        if not row:
            row = LogisticaModel(
                cliente_id=cliente_id,
                frecuencia=frecuencia,
                capacidad_vehiculo=capacidad,
                observ=json.dumps(observ_json or {}, ensure_ascii=False),
            )
            self.db.add(row)
        else:
            row.frecuencia = frecuencia
            row.capacidad_vehiculo = capacidad
            row.observ = json.dumps(observ_json or {}, ensure_ascii=False)
        self.db.commit()
        self.db.refresh(row)
        return row

router = APIRouter(
    prefix="/logistica",
    tags=["logistica"],
    dependencies=[Depends(get_db)],
)

class LogisticaIn(BaseModel):
    frecuencia_resumen: str
    capacidad_kg: Optional[int] = None
    configuracion: Optional[dict[str, Any]] = None

@router.get("/cliente/{cliente_id}")
def get_logistica(cliente_id: int, db: Session = Depends(get_db)):
    svc = LogisticaService(db)
    row = svc.get_by_cliente(cliente_id)
    if not row:
        # Respuesta por defecto si aún no hay config para ese cliente
        return {
            "cliente_id": cliente_id,
            "frecuencia_resumen": None,
            "capacidad_kg": None,
            "configuracion": {
                "tipo": "diaria",
                "dias_semana": [],
                "dias_mes": [],
                "hora_pref": "08:00",
                "ventana_ini": None,
                "ventana_fin": None,
                "veces": 1,
                "cap_estimada": None
            }
        }
    try:
        cfg = json.loads(row.observ or "{}")
    except Exception:
        cfg = {}
    return {
        "cliente_id": cliente_id,
        "frecuencia_resumen": row.frecuencia,
        "capacidad_kg": row.capacidad_vehiculo,
        "configuracion": cfg,
    }

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
