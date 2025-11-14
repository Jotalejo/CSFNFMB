# routers/transporte.py
from fastapi import APIRouter, Depends, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from datetime import date, datetime
from sqlalchemy.orm import Session
from dependencies import get_db, templates
from services.transporte_service import TransporteService # type: ignore
from typing import Optional
from services.plan_transporte_service import PlanTransporteService
from services.transporte_service import TransporteService
from schemas.transporte import PlanResponse, GuardarPlanRequest

router = APIRouter(
    prefix="/transporte",
    tags=["transporte"],
    dependencies=[Depends(get_db)],
)

@router.get("/planilla", response_class=HTMLResponse)
def planilla_transporte(
    request: Request,
    fecha: str = Query(None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    # Determina fecha
    if fecha:
        try:
            dt = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            dt = date.today()
    else:
        dt = date.today()

    svc = TransporteService(db)
    planilla = svc.clientes_programados_para(dt)

    return templates.TemplateResponse(
        "/transporte/planilla.html",
        {
            "request": request,
            "fecha": dt.isoformat(),
            "planilla": planilla
        }
    )

@router.get("/plan", response_model=PlanResponse)
def generar_plan(
    fecha: date = Query(..., description="YYYY-MM-DD"),
    vehiculo_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    buckets = PlanTransporteService(db).generar_plan(fecha, vehiculo_id)
    return {"plan": [b.dict() for b in buckets]}

@router.post("/guardar")
def guardar_plan(req: GuardarPlanRequest, db: Session = Depends(get_db)):
    if not req.plan:
        raise HTTPException(status_code=400, detail="Plan vacío")
    n = TransporteService(db).guardar_plan(req.fecha, req.plan)
    return {"ok": True, "creados": n}
