# routers/citas.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from dependencies import get_db, templates

from services.citas import CitaService
from services.tiposvisita import TipoVisitaService      # usados para cargar catálogos en el form
from services.tipogenerador import TipoGeneradorService # idem
from schemas.Citas import CitaCreate, Cita as CitaSchema

router = APIRouter(
    prefix="/citas",
    tags=["citas"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# -------- Listado HTML (DataTable) --------
@router.get("/")
async def citas_home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("/citas/search.html", {"request": request})

# -------- Listado JSON general --------
@router.get("/json")
async def citas_json(db: Session = Depends(get_db)):
    data = CitaService(db).get_citas()
    return {"data": data}

# -------- Listado JSON por cliente potencial --------
@router.get("/clipot/{clipot_id}/json")
async def citas_by_clipot_json(clipot_id: int, db: Session = Depends(get_db)):
    data = CitaService(db).list_by_clipot(clipot_id)
    return {"data": data}

# -------- Obtener 1 cita (JSON) --------
@router.get("/{cita_id}/json")
async def cita_get_json(cita_id: int, db: Session = Depends(get_db)):
    data = CitaService(db).get_cita(cita_id)
    if not data:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return data

# -------- Form view: nueva cita (con catálogos) --------
@router.get("/nuevo")
async def cita_new_view(
    request: Request,
    clipot_id: Optional[int] = None,
    cliente_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    tiposvisita = TipoVisitaService(db).list_all()
    tipogeneradores = TipoGeneradorService(db).list_all()
    return templates.TemplateResponse(
        "/citas/edit.html",
        {
            "request": request,
            "cita": None,
            "action": "/citas/form",
            "method": "post",
            "tiposvisita": tiposvisita,
            "tipogeneradores": tipogeneradores,
            "pre_clipot_id": clipot_id,
            "pre_cliente_id": cliente_id,
            "url_redirect": router.url_path_for("citas_home"),
        },
    )

# -------- Form view: editar cita (con catálogos) --------
@router.get("/{cita_id}")
async def cita_edit_view(cita_id: int, request: Request, db: Session = Depends(get_db)):
    service = CitaService(db)
    cita = service.get_cita(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    tiposvisita = TipoVisitaService(db).list_all()
    tipogeneradores = TipoGeneradorService(db).list_all()
    return templates.TemplateResponse(
        "/citas/edit.html",
        {
            "request": request,
            "cita": cita,
            "action": "/citas/form",
            "method": "post",
            "tiposvisita": tiposvisita,
            "tipogeneradores": tipogeneradores,
            "url_redirect": router.url_path_for("citas_home"),
        },
    )

# -------- Guardar desde FORM (crear / actualizar) --------
@router.post("/form")
async def cita_form_submit(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    # si viene un hidden cita_id => update; si no => create
    cita_id = form.get("cita_id") or None
    service = CitaService(db)

    if cita_id:
        updated = service.update_from_form(int(cita_id), form)
        if not updated:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        service.create_from_form(form)

    return RedirectResponse(url=router.url_path_for("citas_home"), status_code=303)

# -------- CRUD JSON puro (si lo quieres usar vía API) --------
@router.post("/")
async def cita_create_json(payload: CitaCreate, db: Session = Depends(get_db)):
    return CitaService(db).create(payload)

@router.patch("/{cita_id}")
async def cita_update_json(cita_id: int, payload: CitaSchema, db: Session = Depends(get_db)):
    data = CitaService(db).update(cita_id, payload)
    if not data:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return data

@router.delete("/{cita_id}")
async def cita_delete(cita_id: int, db: Session = Depends(get_db)):
    ok = CitaService(db).delete(cita_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"deleted": True, "id": cita_id}

