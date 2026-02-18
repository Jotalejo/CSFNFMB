# routers/frecuencia.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.Frecuencia import FrecuenciaCreate, FrecuenciaOut, FrecuenciaUpdate
from services.frecuencia_service import FrecuenciaService
from models.FrecuenciaRec import FrecuenciaRec
from typing import List

router = APIRouter(prefix="/frecuencias", tags=["frecuencias"])

def to_out(r: FrecuenciaRec) -> FrecuenciaOut:
    """
    Convierte el modelo FrecuenciaRec a FrecuenciaOut sin reventar cuando diasem_mask es NULL.
    Para mensual (tipo_id=3) diasem_mask normalmente es NULL => from_mask(0) => []
    """
    return FrecuenciaOut(
        id=r.id,
        cliente_id=r.cliente_id,
        tipo_id=r.tipo_id,
        tipo_nombre=r.tipo.nombre if r.tipo else "",
        dias_semana=FrecuenciaRec.from_mask(r.diasem_mask or 0),  # ✅ nunca None
        dias_mes=r.dias_mes,
        hora_desde=r.hora_desde,
        hora_hasta=r.hora_hasta,
        veces=r.veces,
        capacidad_kg=r.capacidad_kg,
        observ=r.observ,
        activo=bool(r.activo),
    )

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
            dias_semana=FrecuenciaRec.from_mask(r.diasem_mask or 0),
            dias_mes=r.dias_mes,
            hora_desde=r.hora_desde,
            hora_hasta=r.hora_hasta,
            veces=r.veces,
            capacidad_kg=r.capacidad_kg,
            observ=r.observ,
            activo=bool(r.activo),
        ))
    return [to_out(r) for r in svc.list_by_cliente(cliente_id)]

@router.post("/", response_model=FrecuenciaOut)
def create_frecuencia(data: FrecuenciaCreate, db: Session = Depends(get_db)):
    svc = FrecuenciaService(db)
    r = svc.create(data)
    return to_out(r)

    #return FrecuenciaOut(
    #    id=r.id,
    #    cliente_id=r.cliente_id,
    #    tipo_id=r.tipo_id,
    #    tipo_nombre=r.tipo.nombre,
    #    dias_semana=FrecuenciaRec.from_mask(r.diasem_mask or 0),
    #    dias_mes=r.dias_mes,
    #    hora_desde=r.hora_desde,
    #    hora_hasta=r.hora_hasta,
    #    veces=r.veces,
    #    capacidad_kg=r.capacidad_kg,
    #    observ=r.observ,
    #    activo=bool(r.activo),
    #)

@router.patch("/", response_model=FrecuenciaOut)
def update_frecuencia(data: FrecuenciaUpdate, db: Session = Depends(get_db)):
    svc = FrecuenciaService(db)
    r = svc.update(data.frecuencia_id, data)
    if not r:
        raise HTTPException(status_code=404, detail="Frecuencia no encontrada")
    return to_out(r)
    
    #return FrecuenciaOut(
    #    id=r.id,
    #    cliente_id=r.cliente_id,
    #    tipo_id=r.tipo_id,
    #    tipo_nombre=r.tipo.nombre,
    #    dias_semana=FrecuenciaRec.from_mask(r.diasem_mask or 0),
    #    dias_mes=r.dias_mes,
    #    hora_desde=r.hora_desde,
    #    hora_hasta=r.hora_hasta,
    #    veces=r.veces,
    #    capacidad_kg=r.capacidad_kg,
    #    observ=r.observ,
    #    activo=bool(r.activo),
    #)