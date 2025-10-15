# routers/frecuencia.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.Frecuencia import FrecuenciaCreate, FrecuenciaOut
from services.frecuencia_service import FrecuenciaService, FrecuenciaRec
from typing import List

router = APIRouter(prefix="/frecuencias", tags=["frecuencias"])

@router.get("/cliente/{cliente_id}", response_model=List[FrecuenciaOut])
def list_by_cliente(cliente_id: int, db: Session = Depends(get_db)):
    svc = FrecuenciaService(db)
    out = []
    for r in svc.list_by_cliente(cliente_id):
        out.append(FrecuenciaOut(
            id=r.id,
            cliente_id=r.cliente_id,
            tipo_id=r.tipo_id,
            tipo_nombre=r.tipo.nombre,
            dias_semana=FrecuenciaRec.from_mask(r.diasem_mask) if r.diasem_mask is not None else None,
            dias_mes=r.dias_mes,
            hora_desde=r.hora_desde,
            hora_hasta=r.hora_hasta,
            veces=r.veces,
            capacidad_kg=r.capacidad_kg,
            observ=r.observ,
            activo=bool(r.activo),
        ))
    return out

@router.post("/", response_model=FrecuenciaOut)
def create_frecuencia(data: FrecuenciaCreate, db: Session = Depends(get_db)):
    svc = FrecuenciaService(db)
    r = svc.create(data)
    return FrecuenciaOut(
        id=r.id,
        cliente_id=r.cliente_id,
        tipo_id=r.tipo_id,
        tipo_nombre=r.tipo.nombre,
        dias_semana=FrecuenciaRec.from_mask(r.diasem_mask) if r.diasem_mask is not None else None,
        dias_mes=r.dias_mes,
        hora_desde=r.hora_desde,
        hora_hasta=r.hora_hasta,
        veces=r.veces,
        capacidad_kg=r.capacidad_kg,
        observ=r.observ,
        activo=bool(r.activo),
    )
