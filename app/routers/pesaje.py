from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from dependencies import templates, get_db
from services import PesajeService
from schemas.pesaje import PesajeCreate


router = APIRouter(
    prefix="/pesaje",
    tags=["pesaje"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def pantalla_pesaje(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "pesaje/pesaje.html",
        {"request": request}
    )


@router.get("/vehiculos")
def vehiculos_por_fecha(fecha: date, db: Session = Depends(get_db)):
    service = PesajeService(db)
    vehiculos = service.get_vehiculos_por_fecha(fecha)

    return [
        {
            "id": v.id,
            "placa": v.placa
        }
        for v in vehiculos
    ]


@router.get("/clientes")
def clientes_por_fecha_vehiculo(
    fecha: date,
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    service = PesajeService(db)
    clientes = service.get_clientes_por_fecha_vehiculo(fecha, vehiculo_id)

    return [
        {
            "id": c.id,
            "razonSocial": c.razonSocial,
            "nit": c.nit
        }
        for c in clientes
    ]


@router.get("/manifiestos")
def manifiestos_por_cliente(
    fecha: date,
    vehiculo_id: int,
    cliente_id: int,
    db: Session = Depends(get_db)
):
    service = PesajeService(db)
    manifiestos = service.get_manifiestos(fecha, vehiculo_id, cliente_id)

    return [
        {
            "id": r.id,
            "fecha": r.fecha.isoformat() if r.fecha else "",
            "hora": r.hora.strftime("%H:%M") if r.hora else "",
            "codigo_barras": r.codigobar or ""
        }
        for r in manifiestos
    ]


@router.get("/detalle-manifiesto/{recoleccion_id}")
def detalle_manifiesto(
    recoleccion_id: int,
    db: Session = Depends(get_db)
):
    service = PesajeService(db)
    detalles = service.get_detalle_manifiesto(recoleccion_id)

    return [
        {
            "id": d.id,
            "tipo_residuo_id": d.tipo_residuo_id,
            "tipo_residuo": d.tipo_residuo.nombre if d.tipo_residuo else "",
            "bolsas": d.cantidad or 0,
            "peso": d.peso_total or d.peso or 0,
            "observaciones": d.observaciones or ""
        }
        for d in detalles
    ]


@router.post("/guardar")
def guardar_pesaje(
    data: PesajeCreate,
    db: Session = Depends(get_db)
):
    if not data.recoleccion_id:
        raise HTTPException(status_code=400, detail="Debe seleccionar un manifiesto")

    if not data.detalles:
        raise HTTPException(status_code=400, detail="No hay residuos para guardar")

    service = PesajeService(db)
    pesaje = service.crear_pesaje(data)

    return {
        "ok": True,
        "mensaje": "Pesaje guardado correctamente",
        "id": pesaje.id
    }


@router.get("/acumulados")
def acumulados(fecha: date, db: Session = Depends(get_db)):
    service = PesajeService(db)

    return {
        "dia": service.acumulado_dia(fecha),
        "semana": service.acumulado_semana(fecha),
        "mes": service.acumulado_mes(fecha),
    }